#import
import discord
from discord.ext import commands


class MyHelpCommand(commands.DefaultHelpCommand):
    def get_command_signature(self, command):
        self.dm_help = True
        self.commands_heading = "Команды:"

        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

class MyCog(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self


def setup(bot):
    bot.add_cog(MyCog(bot))

'''
class Help(commands.Cog):


    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h', 'commands', 'команды'])

def setup(bot):
    bot.add_cog(Help(bot))








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
'''
