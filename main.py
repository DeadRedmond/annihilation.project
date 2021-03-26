#import
import os
import discord
from discord.ext import commands
from pretty_help import PrettyHelp

from settings import token, google_api_key, custom_search_engine
print(f'token: {token}\napi: {google_api_key}\nengine: {custom_search_engine}')

bot = commands.Bot(command_prefix=".", help_command=PrettyHelp(
    active_time=60,
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