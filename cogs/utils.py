#imports
import typing
import discord
from discord.ext import commands

class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #commands
    @commands.command(aliases=['пинг'])
    async def ping(self, ctx):
        """🏓"""
        await ctx.send("🏓 Pong: **{}ms**".format(round(self.bot.latency * 1000, 2)))

    @commands.command(aliases=['эхо'])
    async def echo(self, ctx, *, arg):
        """Повторяю за тобой"""
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.command(aliases= ['бан'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, members: commands.Greedy[discord.Member],
                    delete_days: typing.Optional[int] = 0, *,
                    reason: str):
        """Бан злостных нарушителей\n(удаление сообщений за указанное количество дней - опционально)"""
        for member in members:
            await member.ban(delete_message_days=delete_days, reason=reason)

#setup function
def setup(bot):
    bot.add_cog(Utils(bot))