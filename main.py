#import
import os
import discord
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp


from settings import token, google_api_key, custom_search_engine

menu = DefaultMenu('◀️', '▶️', '❌')
bot = commands.Bot(command_prefix=".", help_command=PrettyHelp(
    navigation=menu,
    active_time=120,
    color=0xa0cfe5))


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
    await bot.change_presence(status = discord.Status.online, activity = discord.Game(".help"))
    print("Online!")

#bot run
bot.run(token)