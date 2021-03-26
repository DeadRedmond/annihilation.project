#import
from discord.ext import commands
from utils.http import freegames

class EGS(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['егс', "халява", "игры", 'games'])
    async def egs(self, ctx):
        '''
        Получить еженедельную халяву из EGS
        '''
        await freegames(ctx)


#setup function
def setup(bot):
    bot.add_cog(EGS(bot))
