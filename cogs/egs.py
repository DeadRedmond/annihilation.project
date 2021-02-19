#import
import asyncio
import aiohttp
import json
import discord
from discord.ext import commands
from datetime import datetime

class EGS(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['егс'])
    async def egs(self, ctx):
        '''
        Получить еженедельную халяву из EGS
        '''
        now=datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions') as resp:
                if resp.status !=200:
                    await ctx.send(f'{ctx.message.author.mention}:confused: Cервис не отвечает.')
                else:
                    result = json.loads(await resp.text())
                    await ctx.send("На этой неделе у нас следующие игры:")
                    for item in result['data']['Catalog']['searchStore']['elements']:
                        if now > datetime.strptime(item['effectiveDate'], '%Y-%m-%dT%H:%M:%S.%fZ'):
                            em = discord.Embed(title=item['title'], url=f"https://www.epicgames.com/store/ru/product/{item['productSlug']}/home", descriptiom=item['description'], color=0xa0cfe5)
                            em.set_image(url=item['keyImages'][2]['url'])
                            await ctx.send("", embed=em)
                        else:
                            continue


#setup function
def setup(bot):
    bot.add_cog(EGS(bot))
