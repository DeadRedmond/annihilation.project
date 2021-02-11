#imports
import typing
import random
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
        if ctx.message.channel.guild.me.manage_messages:
            await ctx.message.delete() #прикрутить проверку на права
        await ctx.send(arg)


    @commands.command(aliases= ['бан'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, members: commands.Greedy[discord.Member],
                    delete_days: typing.Optional[int] = 0, *,
                    reason: str):
        """Бан злостных нарушителей\n(удаление сообщений за указанное количество дней - опционально)"""
        for member in members:
            await member.ban(delete_message_days=delete_days, reason=reason)


    @commands.command(aliases=['шар'])
    async def ball(self, ctx):
        '''Спросить магический шар, предсказывающий будущее.'''
        messages = [":8ball: Несомненно.",
            ":8ball: Это решительно так.",
            ":8ball: Без сомнения.",
            ":8ball: Определенно да.",
            ":8ball: Можешь на это рассчитывать.",
            ":8ball: Насколько я понимаю, да.",
            ":8ball: Скорее всего.",
            ":8ball: Прогноз хороший.",
            ":8ball: Да.",
            ":8ball: Знаки указывают на то, что да.",
            ":8ball: Ответ туманный, попробуйте еще раз.",
            ":8ball: Спросите еще раз позже.",
            ":8ball: Лучше не говорить тебе сейчас.",
            ":8ball: Невозможно предсказать сейчас.",
            ":8ball: Сконцентрируйся и спроси еще раз.",
            ":8ball: Не рассчитывай на это.",
            ":8ball: Ответ отрицательный",
            ':8ball: Мои источники говорят "нет"',
            ":8ball: Прогноз не очень хороший.",
            ":8ball: Очень сомнительно."]
        await ctx.send(messages[random.randint(0, len(messages) - 1)])


    @commands.command(aliases=['монетка'])
    async def coin(self, ctx):
        '''Подбросить монетку'''
        if random.randint(0, 1) == 1:
            await ctx.send(':coin: Орёл!')
        else:
            await ctx.send(':coin: Решка!')


#setup function
def setup(bot):
    bot.add_cog(Utils(bot))