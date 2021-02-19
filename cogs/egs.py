#import
from discord.ext import commands
from cogs.utils.http import freegames

class EGS(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['егс'])
    async def egs(self, ctx):
        '''
        Получить еженедельную халяву из EGS
        '''
        await freegames(ctx)


#setup function
def setup(bot):
    bot.add_cog(EGS(bot))
