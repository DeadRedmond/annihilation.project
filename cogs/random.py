#import
import aiohttp
import json
import discord
from random import randint
from discord.ext import commands

class Random(commands.Cog):
    '''
    RANDOM BULSHIT GO!!!
    '''
    
    def __init__(self, bot):
        self.bot = bot
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


    async def randomimageapi(self, ctx, url: str):
        async with aiohttp.ClientSession(headers=self.header) as session:            
            async with session.get(url) as content:
                if content.status != 200:
                    return await ctx.reply(":confused: Сервис не отвечает.")
                res = json.loads(await content.text())
                try:
                    res['link']
                except:
                    print(f"Error in:\n {content.text}\n\n")
                    return await ctx.reply(":confused: Что-то пошло не так.")
                em = discord.Embed(color=0xa0cfe5)
                em.set_image(url=res['link'])
                await ctx.send("", embed=em)



    @commands.command()
    async def cat(self, ctx):
        """ Posts a random cat """
        await self.randomimageapi(ctx, 'https://some-random-api.ml/img/cat')

    @commands.command()
    async def dog(self, ctx):
        """ Posts a random dog """
        await self.randomimageapi(ctx, 'https://some-random-api.ml/img/dog')

    @commands.command(aliases=["bird"])
    async def birb(self, ctx):
        """ Posts a random birb """
        await self.randomimageapi(ctx, 'https://some-random-api.ml/img/birb')

    @commands.command()
    async def fox(self, ctx):
        """ Posts a random fox """
        await self.randomimageapi(ctx, 'https://some-random-api.ml/img/fox')

    @commands.command(aliases=['мем'])
    async def meme(self, ctx):
        """Posts a random meme"""
        async with aiohttp.ClientSession(headers=self.header) as cs:
            async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as res:
                r = await res.json()
                em = discord.Embed(title="Random meme", color=0xa0cfe5)
                em.set_image(url=r['data']['children'][randint(0, 25)]['data']['url'])
                await ctx.send("", embed=em)


#setup function
def setup(bot):
    bot.add_cog(Random(bot))