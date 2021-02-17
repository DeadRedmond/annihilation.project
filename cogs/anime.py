#import
import aiohttp
import json
import discord
import asyncio
import typing
from discord.ext import commands

from cogs.utils.http import nekoslifeapi, header


class Anime(commands.Cog):
    '''
    Аниме ||и хентай||
    '''

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(aliases=['неко'])
    async def neko(self, ctx):
        """
        neko
        """
        await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/neko')
    
    @commands.command()
    async def anime(self, ctx):
        """
        wallpaper
        """
        await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/wallpaper')

    @commands.command()
    async def fox_girl(self, ctx):
        """
        fox girl
        """
        await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/fox_girl')
    
    @commands.command()
    async def kemonomimi(self, ctx):
        """
        kemonomimi
        """
        await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/kemonomimi')
    
    @commands.command(aliases=['вайфу'])
    async def waifu(self, ctx):
        """
        Получи свою вайфу
        """
        await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/waifu', "Вот твоя вайфу")
    
    @commands.command()
    async def poke(self, ctx, user: typing.Optional[discord.Member]):
        """
        poke
        """
        if user is not None:
            await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/poke', f'{ctx.author} ткнул {user}')
        else:
            await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/poke')
    
    @commands.command()
    async def hug(self, ctx, user: typing.Optional[discord.Member]):
        """
        hug
        """
        if user is not None:
            nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/hug', f'{ctx.author} крепко обнял {user}')
        else:
            await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/hug')
    

    


    '''NSFW COMMANDS!!!'''

    @commands.command(aliases=['хентай'])
    async def hentai(self, ctx):
        """ Random hentai gif """
        if ctx.channel.is_nsfw() or ctx.channel.type is discord.ChannelType.private:
            await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/Random_hentai_gif')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()


    @commands.command()
    async def yuri(self, ctx):
        """ Random yuri gif """
        if ctx.channel.is_nsfw() or ctx.channel.type is discord.ChannelType.private:
            await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/yuri')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()


