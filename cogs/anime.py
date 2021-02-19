#import
import discord
import typing
from discord.ext import commands
from random import randint

from cogs.utils.http import nekoslifeapi, header


class Anime(commands.Cog):
    '''
    Аниме
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def smug(self, ctx):
        """
        smug
        """
        return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/smug')


    @commands.command(aliases=['неко'])
    async def neko(self, ctx):
        """
        neko
        """
        return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/neko')
    
    @commands.command()
    async def anime(self, ctx):
        """
        wallpaper
        """
        return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/wallpaper')

    @commands.command()
    async def fox_girl(self, ctx):
        """
        fox girl
        """
        return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/fox_girl')
    
    @commands.command()
    async def kemonomimi(self, ctx):
        """
        kemonomimi
        """
        return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/kemonomimi')


    """Команды с юзером"""

    @commands.command(aliases=['вайфу'])
    async def waifu(self, ctx, user: typing.Optional[discord.Member]):
        """
        Получи свою вайфу
        """
        if user is not None or user == ctx.author:
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/waifu', f'{ctx.author.mention} выбрал вайфу для {user.mention}')
        else:
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/waifu')
    
    @commands.command()
    async def poke(self, ctx, user: typing.Optional[discord.Member]):
        """
        poke
        """
        if user is None:
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/poke')
        elif user == ctx.author:
            text=f'Тыкаем пальцем в {user.mention}'
        else:
            text=f'{ctx.author.mention} ткнул пальцем в {user.mention}'
        return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/poke', text)

    @commands.command()
    async def hug(self, ctx, user: typing.Optional[discord.Member]):
        """
        hug
        """
        urls=['https://nekos.life/api/v2/img/hug', 'https://nekos.life/api/v2/img/cuddle']

        if user is None:
            return await nekoslifeapi(ctx, f'{urls[randint(0, 1)]}')
        elif user == ctx.author:
            text=f'{user.mention} хочет что бы его обняли. Вот, держи свою порцию.'
        else:
            text=f'{ctx.author.mention} вдруг решил обнять {user.mention}'
        return await nekoslifeapi(ctx, f'{urls[randint(0, 1)]}', text)


    @commands.command()
    async def pat(self, ctx, user: typing.Optional[discord.Member]):
        """
        pat
        """
        if user is None:
            return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/pat')
        elif user == ctx.author:
            text=f'{user.mention} хочет что бы его погладили. Ну давай, иди сюда'
        else:
            text=f'{ctx.author.mention} неожиданно решил погладить {user.mention}'
        return await nekoslifeapi(ctx, 'https://nekos.life/api/v2/img/pat', text)


    

#setup function
def setup(bot):
    bot.add_cog(Anime(bot))
