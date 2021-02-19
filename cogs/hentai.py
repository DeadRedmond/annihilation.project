#import
import asyncio
import discord
from discord.ext import commands
from random import randint

from cogs.utils.http import nekoslifeapi, header


class Hentai(commands.Cog):
    '''
    Хентай, только для NSFW-каналов!
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['хентай'])
    @commands.is_nsfw()
    async def hentai(self, ctx):
        """ Random hentai """
        urls=['https://nekos.life/api/v2/img/classic', 'https://nekos.life/api/v2/img/Random_hentai_gif']
        if ctx.channel.type is discord.ChannelType.private or ctx.channel.is_nsfw():
            return await nekoslifeapi(ctx, f'{urls[randint(0, 1)]}')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()


    @commands.command()
    @commands.is_nsfw()
    async def yuri(self, ctx):
        """ Random yuri """
        if ctx.channel.type is discord.ChannelType.private or ctx.channel.is_nsfw():
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/yuri')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()

    @commands.command()
    @commands.is_nsfw()
    async def tits(self, ctx):
        """ Random hentai tits """
        if ctx.channel.type is discord.ChannelType.private or ctx.channel.is_nsfw():
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/tits')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()

    @commands.command()
    @commands.is_nsfw()
    async def feet(self, ctx):
        """ Тут есть фут-фетишисты??? """
        if ctx.channel.type is discord.ChannelType.private or ctx.channel.is_nsfw():
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/feet')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()

    @commands.command(alias='анал')
    @commands.is_nsfw()
    async def anal(self, ctx):
        """ Anal hentai """
        if ctx.channel.type is discord.ChannelType.private or ctx.channel.is_nsfw():
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/anal')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()

    @commands.command(alias='blowjob')
    @commands.is_nsfw()
    async def bj(self, ctx):
        """ Blowjob hentai """
        urls=['https://nekos.life/api/v2/img/bj', 'https://nekos.life/api/v2/img/blowjob']
        if ctx.channel.type is discord.ChannelType.private or ctx.channel.is_nsfw():
            return await nekoslifeapi(ctx, f'{urls[randint(0, 1)]}')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()
    

    @commands.command()
    @commands.is_nsfw()
    async def pwankg(self, ctx):
        """ hentai pwankg """
        if ctx.channel.type is discord.ChannelType.private or ctx.channel.is_nsfw():
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/pwankg')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()

    @commands.command()
    @commands.is_nsfw()
    async def spank(self, ctx):
        """ hentai spank """
        if ctx.channel.type is discord.ChannelType.private or ctx.channel.is_nsfw():
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/spank')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()


    @commands.command()
    @commands.is_nsfw()
    async def trap(self, ctx):
        """ It's a trap! """
        if ctx.channel.type is discord.ChannelType.private or ctx.channel.is_nsfw():
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/trap')
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()




#setup function
def setup(bot):
    bot.add_cog(Hentai(bot))
