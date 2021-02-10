from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
import json

class Search:
    """Reverse image search commands"""


    def __init__(self, bot):
        self.bot = bot
        self.sauce_session = aiohttp.ClientSession()
        self.tineye_session = aiohttp.ClientSession()

    
    def __unload(self):
        self.sauce_session.close()
        self.tineye_session.close()


    def _tag_to_title(self, tag):
        return tag.replace(' ', ', ').replace('_', ' ').title()

    
    @commands.command(pass_context=True)
    async def sauce(self, ctx, link=None, similarity=80):
        """
        reverse image search via saucenao
       usage:   .sauce <image-link> <similarity (in percent)> or
                .sauce on image upload comment <similarity (in percent)>
        """
        file = ctx.message.attachments
        if link is None and not file:
            await self.bot.say('Message didn\'t contain Image')
        else:
            await self.bot.type()
            if file:
                url = file[0]['proxy_url']
                similarity = link
            else:
                url = link
            async with self.sauce_session.get('http://saucenao.com/search.php?url={}'.format(url)) as response:
                source = None
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    for result in soup.select('.resulttablecontent'):
                        if float(similarity) > float(result.select('.resultsimilarityinfo')[0].contents[0][:-1]):
                            break
                        else:
                            if result.select('a'):
                                source = result.select('a')[0]['href']
                                await self.bot.reply('<{}>'.format(source))
                                return
                    if source is None:
                        await self.bot.reply('No source over the similarity threshold')

    @commands.command(pass_context=True)
    async def tineye(self, ctx, link=None):
        """
        reverse image search using tineye
        usage:  .tineye <image-link> or
                .tineye on image upload comment
        """
        file = ctx.message.attachments
        if link is None and not file:
            await self.bot.say('Message didn\'t contain Image')
        else:
            await self.bot.type()
            if file:
                url = file[0]['proxy_url']
            else:
                url = link
            async with self.tineye_session.get('https://tineye.com/search/?url={}'.format(url)) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                pages = []
                image_link = None
                for hidden in soup.find(class_='match').select('.hidden-xs'):
                    if hidden.contents[0].startswith('Page:'):
                        pages.append('<{}>'.format(hidden.next_sibling['href']))
                    else:
                        image_link = hidden.a['href']
            message = '\n**Pages:** '
            message += '\n**Pages:** '.join(pages)
            if image_link is not None:
                message += '\n**direct image:** <{}>'.format(image_link)
            await self.bot.reply(message)


def setup(bot):
    bot.add_cog(Search(bot))