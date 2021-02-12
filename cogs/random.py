#import
import aiohttp
import json
import discord
from discord.ext import commands

class Random(commands.Cog):
    '''
    RANDOM BULSHIT GO!!!
    '''
    
    def __init__(self, bot):
        self.bot = bot

    async def randomimageapi(self, ctx, url: str):
        session = aiohttp.ClientSession()
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



#setup function
def setup(bot):
    bot.add_cog(Random(bot))