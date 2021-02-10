#import
import os
import requests
import urllib.parse
import discord
import json
from discord.ext import commands
from bs4 import BeautifulSoup

'''Module for google web and image search.'''

google_api_key = os.getenv("SEARCH_API")
custom_search_engine = os.getenv("SEARCH_ENGINE")

class Google(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['google', 'search', 'гугл'])
    async def g(self, ctx, *, query):
        """Google web search"""
        #input = "https://www.googleapis.com/customsearch/v1?q=" + urllib.parse.quote_plus(query) + "&start=1" + "&key=" + google_api_key + "&cx=" + custom_search_engine
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
            em.add_field(name='1. ' + result['items'][0]['title'], value='['+result['items'][0]['link']+']('+result['items'][0]['link']+')' ,inline=False)
            em.add_field(name='2. ' + result['items'][1]['title'], value='['+result['items'][1]['link']+']('+result['items'][0]['link']+')' ,inline=False)
            em.add_field(name='3. ' + result['items'][2]['title'], value='['+result['items'][2]['link']+']('+result['items'][0]['link']+')' ,inline=False)
            
            await ctx.send(f'{ctx.message.author.mention}, вот что мне удалось найти:', embed=em)
        
        
        '''searchInput = "https://google.com/search?q="+urllib.parse.quote(query)
        res = requests.get(searchInput)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        linkElements = soup.select('div#main > div > div > div > a')
        if len(linkElements) == 0:
            await ctx.send("Couldn't find any results...")
        else:
            link = linkElements[0].get("href")
            i = 0
            while link[0:4] != "/url" or link[14:20] == "google":
                i += 1
                link = linkElements[i].get("href")
            await ctx.send(":desktop: http://google.com"+link)'''


#setup function
def setup(bot):
    bot.add_cog(Google(bot))