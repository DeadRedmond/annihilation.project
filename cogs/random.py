#import
import asyncio
import aiohttp
import json
import discord
from random import randint
from discord.ext import commands

from cogs.utils.http import randomimageapi, nekoslifeapi, header

class Random(commands.Cog):
    '''
    RANDOM BULSHIT GO!!!
    '''
    
    def __init__(self, bot):
        self.bot = bot
        #self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


    @commands.command(aliases=['кот', '🐱'])
    async def cat(self, ctx):
        """ Постим котиков 🐱"""
        if randint(0, 1) == 0: #используем случайное апи
            await randomimageapi(ctx, 'https://some-random-api.ml/img/cat')
        else:
            await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/meow')

    @commands.command(aliases=[':dog:', "🐶"])
    async def dog(self, ctx):
        """ Постим собак 🐶"""
        if randint(0, 1) == 0: #используем случайное апи
            await randomimageapi(ctx, 'https://some-random-api.ml/img/dog')
        else:
            await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/woof')

    @commands.command(aliases=["bird", "птица", "птиц", "🐦"])
    async def birb(self, ctx):
        """ Постим птиц 🐦"""
        await randomimageapi(ctx, 'https://some-random-api.ml/img/birb')

    @commands.command(aliases=["лис", "лиса", "🦊"])
    async def fox(self, ctx):
        """ Постим лис 🦊"""
        await randomimageapi(ctx, 'https://some-random-api.ml/img/fox')

    @commands.command(aliases=["гусь"])
    async def goose(self, ctx):
        """ Постим гуся """
        await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/goose')

    @commands.command(aliases=["ящурка", "🦎"])
    async def lizard(self, ctx):
        """ Постим ящурок 🦎"""
        await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/lizard')

    @commands.command(aliases=["frog", "легушка", "🐸"])
    async def forg(self, ctx):
        """Постим легущек 🐸"""
        em = discord.Embed(color=0xa0cfe5)
        tmp = randint(0, 54)
        em.set_image(url=f"http://www.allaboutfrogs.org/funstuff/random/00{tmp:02d}.jpg")
        await ctx.send("", embed=em)

    


    @commands.command(aliases=["мем"])
    async def meme(self, ctx):
        """Постит случайную картинку с r/memes"""
        async with aiohttp.ClientSession(headers=header) as cs:
            async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as res:
                r = await res.json()
                url = r['data']['children'][randint(0, 25)]['data']['url']
                if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    em = discord.Embed(color=0xa0cfe5)
                    em.set_image(url=url)
                    await ctx.send("", embed=em)
                else:
                    await ctx.send(url)


    
    @commands.command(aliases=["нсфв"])
    async def nsfw(self, ctx):
        """Постит случайную картинку с r/nsfw"""
        if ctx.channel.is_nsfw() or ctx.channel.type is discord.ChannelType.private:
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
    bot.add_cog(Random(bot))