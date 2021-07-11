#import
import asyncio
import aiohttp
import discord
from discord.ext import commands
from random import randint
from cogs.utils.http import nekoslifeapi, header

class NSFW(commands.Cog):
    '''
    Только для NSFW-каналов!
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

    @commands.is_nsfw()
    @commands.command(aliases=["нсфв"])
    async def nsfw(self, ctx):
        """Постит случайную картинку с r/nsfw"""
        if ctx.channel.type is discord.ChannelType.private or ctx.channel.is_nsfw():
            async with aiohttp.ClientSession(headers=header) as cs:
                async with cs.get('https://www.reddit.com/r/nsfw/new.json?sort=hot') as res:
                    r = await res.json()
                    url = r['data']['children'][randint(0, 25)]['data']['url']
                    if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        em = discord.Embed(color=0xa0cfe5)
                        em.set_image(url=url)
                        await ctx.send("", embed=em)
                    else:
                        await ctx.send(url)
        else:
            message = await ctx.reply("Эту команду можно искользовать только в NSFW-каналах")
            if ctx.message.channel.guild.me.guild_permissions.manage_messages:
                await asyncio.sleep(10)
                await ctx.message.delete()
                await message.delete()



#setup function
def setup(bot):
    bot.add_cog(NSFW(bot))
