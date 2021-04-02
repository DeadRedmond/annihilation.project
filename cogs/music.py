#v0.1
import asyncio
import random
import re
import typing
from enum import Enum
from discord.ext import commands
import discord
import youtube_dl as ytdl
from math import ceil as ceil




URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

YTDL_config = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}

FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

# Silence useless bug reports messages
ytdl.utils.bug_reports_message = lambda: ''


class GuildState:
    """Helper class managing per-guild state."""

    def __init__(self):
        self.playlist = []
        self.skip_votes = set()
        self.now_playing = None

    def is_requester(self, user):
        return self.now_playing.requested_by == user

class Video:
    """Class containing information about a particular video."""

    def __init__(self, url_or_search, requested_by):
        """Plays audio from (or searches for) a URL."""
        with ytdl.YoutubeDL(YTDL_config) as ydl:
            video = self._get_info(url_or_search)
            video_format = video["formats"][0]
            self.stream_url = video_format["url"]
            self.video_url = video["webpage_url"]
            self.title = video["title"]
            self.uploader = video["uploader"] if "uploader" in video else ""
            self.thumbnail = video["thumbnail"] if "thumbnail" in video else None
            self.requested_by = requested_by

    def _get_info(self, video_url):
        with ytdl.YoutubeDL(YTDL_config) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                return self._get_info(
                    info["entries"][0]["url"])  # get info for first video
            else:
                video = info
            return video

    def get_embed(self):
        """Makes an embed out of this Video's information."""
        embed = discord.Embed(
            title=self.title, description=self.uploader, url=self.video_url)
        embed.set_footer(
            text=f"Requested by {self.requested_by.name}",
            icon_url=self.requested_by.avatar_url)
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        return embed


async def audio_playing(ctx):
    """Checks that audio is currently playing before continuing."""
    client = ctx.guild.voice_client
    if client and client.channel and client.source:
        return True
    else:
        raise commands.CommandError("Сейчас ничего не играет")

async def in_voice_channel(ctx):
    """Checks that the command sender is in the same voice channel as the bot."""
    voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client
    if voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel:
        return True
    else:
        raise commands.CommandError(
            "Для этой команды необходимо быть в голосовом канале.")

async def is_audio_requester(ctx):
    """Checks that the command sender is the song requester."""
    music = ctx.bot.get_cog("Music")
    state = music.get_state(ctx.guild)
    permissions = ctx.channel.permissions_for(ctx.author)
    if permissions.administrator or state.is_requester(ctx.author):
        return True
    else:
        raise commands.CommandError(
            "Для этой команды необходимо быть заказчиком")

def _queue_text(self, queue):
        """Возвращает текущую композицию."""
        if len(queue) > 0:
            message = [f"{len(queue)} треков в очереди:"]
            message += [
                f"  {index+1}. **{song.title}** (заказан **{song.requested_by.name}**)"
                for (index, song) in enumerate(queue)
            ]  # add individual songs
            return "\n".join(message)
        else:
            return "Очередь воспроизведения пустая."


class Music(commands.Cog):
    "Музыка! :musical_note: "

    def __init__(self, bot):
        self.bot = bot
        self.states = {}

    def get_state(self, guild):
        """Gets the state for `guild`, creating it if it does not exist."""
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
        return self.states[guild.id]
    
    def _queue_text(self, queue):
        """Возвращает текущую композицию."""
        if len(queue) > 0:
            message = [f"{len(queue)} треков в очереди:"]
            message += [
                f"  {index+1}. **{song.title}** (заказан **{song.requested_by.name}**)"
                for (index, song) in enumerate(queue)
            ]  # add individual songs
            return "\n".join(message)
        else:
            return "Очередь воспроизведения пустая."
        
    def _play_song(self, client, state, song):
        state.now_playing = song
        state.skip_votes = set()  # clear skip votes
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url))

        def after_playing(err):
            if len(state.playlist) > 0:
                next_song = state.playlist.pop(0)
                self._play_song(client, state, next_song)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(), self.bot.loop)
        client.play(source, after=after_playing)


    def _pause_audio(self, client):
        if client.is_paused():
            client.resume()
        else:
            client.pause()

    def _vote_skip(self, channel, member):
        """Register a vote for `member` to skip the song playing."""
        state = self.get_state(channel.guild)
        state.skip_votes.add(member)
        users_in_channel = len([member for member in channel.members if not member.bot])  # don't count bots
        if (float(len(state.skip_votes)) / users_in_channel) >= 0.5:
            # enough members have voted to skip, so skip the song
            channel.guild.voice_client.stop()

    @commands.command(brief="Играть музыку с указанного <url>.")
    @commands.guild_only()
    async def play(self, ctx, *, url):
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)  # get the guild's state

        if client and client.channel:
            try:
                video = Video(url, ctx.author)
            except ytdl.DownloadError as e:
                await ctx.send("Ошибка загрузки.")
                return
            state.playlist.append(video)
            #await ctx.send("Added to queue.", embed=video.get_embed())
            await ctx.send("Added to queue.") #не выводим embed
        else:
            if ctx.author.voice is not None and ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel
                try:
                    video = Video(url, ctx.author)
                except ytdl.DownloadError as e:
                    await ctx.send("Ошибка загрузки.")
                    return
                client = await channel.connect()
                self._play_song(client, state, video)
                #await ctx.send("Added to queue.", embed=video.get_embed())
                await ctx.send("Added to queue.") #не выводим embed
            else:
                raise commands.CommandError("You need to be in a voice channel to do that.")
            
    @commands.command(aliases=["resume", "p"])
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    @commands.check(is_audio_requester)
    async def pause(self, ctx):
        """Pauses any currently playing audio."""
        client = ctx.guild.voice_client
        self._pause_audio(client)

    @commands.command()
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def skip(self, ctx):
        """Пропустить текущий трек"""
        state = self.get_state(ctx.guild)
        client = ctx.guild.voice_client
        if ctx.channel.permissions_for(
                ctx.author).administrator or state.is_requester(ctx.author):
            # immediately skip if requester or admin
            client.stop()

        else:
            # vote to skip song
            channel = client.channel
            self._vote_skip(channel, ctx.author)
            # announce vote
            users_in_channel = len([
                member for member in channel.members if not member.bot
            ])  # don't count bots
            required_votes = ceil(0.5 * users_in_channel)
            await ctx.send(f"{ctx.author.mention} voted to skip ({len(state.skip_votes)}/{required_votes} votes)")

    @commands.command()
    @commands.guild_only()
    @commands.check(audio_playing)
    async def np(self, ctx):
        """Выводит текущую композицию."""
        state = self.get_state(ctx.guild)
        await ctx.send("", embed=state.now_playing.get_embed())

    @commands.command(aliases=["q", "playlist"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def queue(self, ctx):
        """Выводит очередь."""
        state = self.get_state(ctx.guild)
        await ctx.send(self._queue_text(state.playlist))

    @commands.command(aliases=["cq"])
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.has_permissions(administrator=True)
    async def clearqueue(self, ctx):
        """Clears the play queue without leaving the channel."""
        state = self.get_state(ctx.guild)
        state.playlist = []

    @commands.command(aliases=["stop"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        """Выгнать бота с голосового канала."""
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)
        if client and client.channel:
            await client.disconnect()
            state.playlist = []
            state.now_playing = None
        else:
            raise commands.CommandError("Не в голосовом команде")

    



#setup function
def setup(bot):
    bot.add_cog(Music(bot))