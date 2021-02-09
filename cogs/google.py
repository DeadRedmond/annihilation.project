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
        result = requests.get("https://www.googleapis.com/customsearch/v1?q=" + urllib.parse.quote_plus(query) + "&start=1" + "&key=" + google_api_key + "&cx=" + custom_search_engine) as resp:
        result = json.loads(await resp.text())
        ctx.send(result['items'][0]['link'])
        
        
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