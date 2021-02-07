#import
import os
import discord
import typing
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
token = os.getenv("BOT_TOKEN")

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game("Annihilation!"))
    print("Online!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong!🏓 Latency: {str(round(bot.latency, 2))}")

@bot.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)

@bot.command(pass_context=True)
@commands.has_role("test")
async def check(ctx, user: discord.Member):
    role = discord.utils.find(lambda r: r.name == 'название_роли', ctx.message.server.roles)
    if role in user.roles:
        await ctx.send("у вас есть роль")
    else:
        await ctx.send("у вас нету роли")

"""Mass bans members with an optional delete_days parameter"""
"""@bot.command()
@commands.check_any(commands.is_owner(), is_guild_owner())
async def ban(ctx, members: commands.Greedy[discord.Member],
                   delete_days: typing.Optional[int] = 0, *,
                   reason: str):
    for member in members:
        await member.ban(delete_message_days=delete_days, reason=reason)
"""

bot.run(token)
