#import
import os
import requests
import urllib.parse
import discord
import json
import random
from discord.ext import commands
from bs4 import BeautifulSoup

google_api_key = os.getenv("SEARCH_API")
custom_search_engine = os.getenv("SEARCH_ENGINE")

class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['google', 'search', 'гугл'])
    async def g(self, ctx, *, query):
        """Поиск в Гугле"""
        resp = requests.get(f"https://www.googleapis.com/customsearch/v1?q={urllib.parse.quote_plus(query)}&start=1&key={google_api_key}&cx={custom_search_engine}")
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
            em.set_footer(text="Запрос: \"" + query + "\"")
            await ctx.send(f'{ctx.message.author.mention}, вот что мне удалось найти:', embed=em)
        
    @commands.command(aliases = ['image', 'img', 'картинка'])
    async def i(self, ctx, *, query):
        """Поиск картинок в Гугле"""
        resp = requests.get(f"https://www.googleapis.com/customsearch/v1?q={urllib.parse.quote_plus(query)}&start=1&key={google_api_key}&cx={custom_search_engine}&searchType=image")
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



    @commands.command(pass_context=True)
    async def xkcd(self, ctx, *, comic=""):
        """Достаём комикс xkcd."""
        print(f'Комикс:{comic}')
        if comic == "random" or comic == "рандом":
            randcomic = requests.get("https://c.xkcd.com/random/comic/")
            comic = randcomic.url.split("/")[-2]
        site = requests.get(f"https://xkcd.com/{comic}/info.0.json")
        if site.status_code == 404:
            site = None
            found = None
            search = urllib.parse.quote(comic)
            result = (requests.get(f"https://www.google.com/search?&q={search}+site:xkcd.com")).text
            soup = BeautifulSoup(result, "html.parser")
            links = soup.find_all("cite")
            for link in links:
                if link.text.startswith("https://xkcd.com/"):
                    found = link.text.split("/")[3]
                    break
            if not found:
                await ctx.send(":confused: Такого комикса нету")
            else:
                site = requests.get(f"https://xkcd.com/{found}/info.0.json")
                comic = found
        if site:
            json = site.json()
            embed = discord.Embed(title="xkcd {}: {}".format(json["num"], json["title"]), url="https://xkcd.com/{}".format(comic))
            embed.set_image(url=json["img"])
            embed.set_footer(text="{}".format(json["alt"]))
            await ctx.send("", embed=embed)



#setup function
def setup(bot):
    bot.add_cog(Search(bot))