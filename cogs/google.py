#import
import os
import requests
import urllib.parse
import discord
import json
import random
from discord.ext import commands

google_api_key = os.getenv("SEARCH_API")
custom_search_engine = os.getenv("SEARCH_ENGINE")

class Google(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['google', 'search', 'гугл'])
    async def g(self, ctx, *, query):
        """Поиск в Гугле"""
        resp = requests.get("https://www.googleapis.com/customsearch/v1?q=" + urllib.parse.quote_plus(query) + "&start=1" + "&key=" + google_api_key + "&cx=" + custom_search_engine)
        if resp.status_code !=200:
            await ctx.send(f'{ctx.message.author.mention}:confused: Поиск невозможен, сервис не отвечает.')
        else:        
            result = json.loads(resp.text)
            try:
                result['items']
            except:
                return await ctx.send(f'{ctx.message.author.mention} :thinking: Интернет не в курсе, поищите что-то другое.')
            if len(result['items']) < 1:
                return await ctx.send(f'{ctx.message.author.mention} :thinking: Интернет не в курсе, поищите что-то другое.')
            em = discord.Embed(color=0x992d22)
            for i in range(3):
                em.add_field(name=f'{i+1}. {result["items"][i]["title"]}', value=f'[{result["items"][i]["link"]}]({result["items"][i]["link"]})', inline=False)
            await ctx.send(f'{ctx.message.author.mention}, вот что мне удалось найти:', embed=em)
        
    @commands.command(aliases = ['image', 'img', 'картинка'])
    async def i(self, ctx, *, query):
        """Поиск картинок в Гугле"""
        resp = requests.get("https://www.googleapis.com/customsearch/v1?q=" + urllib.parse.quote_plus(query) + "&start=1" + "&key=" + google_api_key + "&cx=" + custom_search_engine + "&searchType=image")
        if resp.status_code !=200:
            await ctx.send(f'{ctx.message.author.mention}:confused: Поиск невозможен, сервис не отвечает.')
        else: 
            result = json.loads(resp.text)
            try:
                result['items']
            except:
                return await ctx.send(f'{ctx.message.author.mention} :thinking: Интернет не в курсе, поищите что-то другое.')
            amount = len(result['items'])
            if amount < 1:
                return await ctx.send(f'{ctx.message.author.mention} :thinking: Интернет не в курсе, поищите что-то другое.')
            em = discord.Embed(color=0x992d22)
            item = random.randint(0, amount)
            em.set_image(url=result['items'][item]['link'])
            em.set_footer(text="Запрос: \"" + query + "\"")
            await ctx.send(f'{ctx.message.author.mention}, вот что мне удалось найти:', embed=em)


#setup function
def setup(bot):
    bot.add_cog(Google(bot))