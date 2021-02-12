#import
import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="n/")
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
    await bot.change_presence(status = discord.Status.online, activity = discord.Game("n/help"))
    print("Online!")

#bot run
bot.run(token)