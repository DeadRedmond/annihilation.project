#import
import os
import discord
import typing
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
token = os.getenv("BOT_TOKEN")

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game("Annihilation!"))
    print("Online!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong!🏓 Latency: {str(round(bot.latency, 2))}")

@bot.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)

"""Mass bans members with an optional delete_days parameter"""
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, members: commands.Greedy[discord.Member],
                   delete_days: typing.Optional[int] = 0, *,
                   reason: str):
    for member in members:
        await member.ban(delete_message_days=delete_days, reason=reason)
@commands.ban.brief("Mass bans members with an optional delete_days parameter")

bot.run(token)