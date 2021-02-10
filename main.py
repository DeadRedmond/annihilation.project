#import
import os
import discord
import typing
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
token = os.getenv("BOT_TOKEN")

#enable cogs
for extension in os.listdir("cogs"):
    if extension.endswith(".py"):
        try:
            bot.load_extension("cogs." + extension[:-3])
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))


#events
@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game("Annihilation!"))
    print("Online!")

#commands
@bot.command(aliases=['пинг'])
async def ping(ctx):
    """🏓"""
    await ctx.send("🏓 Pong: **{}ms**".format(round(bot.latency * 1000, 2)))

@bot.command(aliases=['эхо'])
async def echo(ctx, *, arg):
    """Повторяю за тобой"""
    await ctx.message.delete()
    await ctx.send(arg)

@bot.command(aliases= ['бан'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, members: commands.Greedy[discord.Member],
                   delete_days: typing.Optional[int] = 0, *,
                   reason: str):
    """Бан злостных нарушителей (удаление сообщений за указанное количество дней - опционально)"""
    for member in members:
        await member.ban(delete_message_days=delete_days, reason=reason)


#bot run
bot.run(token)