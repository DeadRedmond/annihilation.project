#import
import os
import requests
import urllib.parse
import discord
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
        searchInput = "https://google.com/search?q="+urllib.parse.quote(query)
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
            await ctx.send(":desktop: http://google.com"+link)
