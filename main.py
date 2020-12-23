#import
import os
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="!")
token = os.getenv("BOT_TOKEN")

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Annihilation!"))
    print("Online!")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong!🏓 Latency: {str(round(client.latency, 2))}")

client.run(token)