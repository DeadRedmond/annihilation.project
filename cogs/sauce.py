from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup

class Search(commands.Cog):
    """Reverse image search commands"""


    def __init__(self, bot):
        self.bot = bot
        self.sauce_session = aiohttp.ClientSession()
        self.tineye_session = aiohttp.ClientSession()

    
    def __unload(self):
        self.sauce_session.close()
        self.tineye_session.close()

    
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
        async with self.sauce_session.get(f'http://saucenao.com/search.php?url={url}') as response:
            source = None
            if response.status != 200:
                await ctx.send(":confused: Поиск невозможен, сервис не отвечает.")
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