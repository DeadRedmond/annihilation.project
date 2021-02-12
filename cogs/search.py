#import
import os
import requests
import aiohttp
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
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


    @commands.command(aliases = ['google', 'search', 'гугл'])
    async def g(self, ctx, *, query):
        """Поиск в Гугле"""
        
        #resp = requests.get(f"https://www.googleapis.com/customsearch/v1?q={urllib.parse.quote_plus(query)}&start=1&key={google_api_key}&cx={custom_search_engine}")

        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(f"https://www.googleapis.com/customsearch/v1?q={urllib.parse.quote_plus(query)}&start=1&key={google_api_key}&cx={custom_search_engine}") as resp:
                if resp.status() !=200:
                    await ctx.send(f'{ctx.message.author.mention}:confused: Поиск невозможен, сервис не отвечает.')
                else:        
                    result = json.loads(await resp.text())
                    try:
                        result['items']
                    except:
                        return await ctx.send(f'{ctx.message.author.mention} :thinking: Интернет не в курсе, поищите что-то другое.')
                    if len(result['items']) < 1:
                        return await ctx.send(f'{ctx.message.author.mention} :thinking: Интернет не в курсе, поищите что-то другое.')
                    em = discord.Embed(color=0xa0cfe5)
                    for i in range(3):
                        em.add_field(name=f'{i+1}. {result["items"][i]["title"]}', value=f'[{result["items"][i]["link"]}]({result["items"][i]["link"]})', inline=False)
                    em.set_footer(text="Запрос: \"" + query + "\"")
                    await ctx.send(f'{ctx.message.author.mention}, вот что мне удалось найти:', embed=em)


    @commands.command(aliases = ['image', 'img', 'картинка'])
    async def i(self, ctx, *, query):
        """Поиск картинок в Гугле"""
        #resp = requests.get(f"https://www.googleapis.com/customsearch/v1?q={urllib.parse.quote_plus(query)}&start=1&key={google_api_key}&cx={custom_search_engine}&searchType=image")
        
        
        
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(f"https://www.googleapis.com/customsearch/v1?q={urllib.parse.quote_plus(query)}&start=1&key={google_api_key}&cx={custom_search_engine}&searchType=image") as resp:
                if resp.status() !=200:
                    await ctx.send(f'{ctx.message.author.mention}:confused: Поиск невозможен, сервис не отвечает.')
                else:        
                    result = json.loads(await resp.text())
                    try:
                        result['items']
                    except:
                        return await ctx.send(f'{ctx.message.author.mention} :thinking: Интернет не в курсе, поищите что-то другое.')
                    amount = len(result['items'])
                    if amount < 1:
                        return await ctx.send(f'{ctx.message.author.mention} :thinking: Интернет не в курсе, поищите что-то другое.')
                    em = discord.Embed(color=0xa0cfe5)
                    item = random.randint(0, amount)
                    em.set_image(url=result['items'][item]['link'])
                    em.set_footer(text="Запрос: \"" + query + "\"")
                    await ctx.send(f'{ctx.message.author.mention}, вот что мне удалось найти:', embed=em)



    @commands.command(pass_context=True)
    async def xkcd(self, ctx, *, comic=""):
        """Достаём комикс xkcd."""
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
            embed = discord.Embed(title=f"xkcd {json['num']}: {json['title']}", url=f"https://xkcd.com/{comic}", color=0xa0cfe5)
            embed.set_image(url=json["img"])
            embed.set_footer(text=f"{json['alt']}")
            await ctx.send("", embed=embed)
    

    @commands.command(pass_context=True, aliases=['соус'])
    async def sauce(self, ctx, link=None, similarity=75):
        """
        Ищем соус, точность по умолчанию 75%
        (картинку можно просто прилепить к сообщению)
        """
        
        file = ctx.message.attachments

        if len(file)==0:
            if link is None:
                return await ctx.reply('А где картинка то?', mention_author=True)
            url = link
        else:
            url = file[0].url
            if link is not None:
                similarity = link

        try:
            similarity = float(similarity)
        except ValueError:
            return await ctx.reply(':warning: Неверно указана точность поиска.')
        
        #print(f'URL={url}\nSimilaraty={similarity}') #debug message

        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(f'http://saucenao.com/search.php?url={url}') as response:
                source = None
                if response.status != 200:
                    return await ctx.send(":confused: Поиск невозможен, сервис не отвечает.")
                else:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    for result in soup.select('.resulttablecontent'):
                        if similarity > float(result.select('.resultsimilarityinfo')[0].contents[0][:-1]):
                            break
                        else:
                            if result.select('a'):
                                source = result.select('a')[0]['href']
                                return await ctx.reply(f'<{source}>', mention_author=True) ###Заменить на embedded       
                    if source is None:
                        return await ctx.reply(":confused: С заданным показателем точности ничего не найдено", mention_author=True)






#setup function
def setup(bot):
    bot.add_cog(Search(bot))