#import
import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="n/", help_command=None)
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


@bot.command()
async def help(ctx, args=None):
    help_embed = discord.Embed()
    command_names_list = [x.name for x in bot.commands]

    # If there are no arguments, just list the commands:
    if not args:
        help_embed.add_field(
            name="Список всех команд:",
            value="\n".join([str(i+1)+". "+x.name for i,x in enumerate(bot.commands)]),
            inline=False
        )
        help_embed.add_field(
            name="Детали",
            value="Введие`n/help <команда>` для более подробной информации о каждой команде.",
            inline=False
        )

    # If the argument is a command, get the help text from that command:
    elif args in command_names_list:
        help_embed.add_field(
            name=args,
            value=bot.get_command(args).help
        )

    # If someone is just trolling:
    else:
        help_embed.add_field(
            name=":warning:",
            value="Кажется здесь такой команды нет"
        )

    await ctx.send(embed=help_embed)



#bot run
bot.run(token)