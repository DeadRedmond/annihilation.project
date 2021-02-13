import aiohttp
import json
import discord


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

async def randomimageapi(ctx, url: str):
    async with aiohttp.ClientSession(headers=header) as session:            
        async with session.get(url) as content:
            if content.status != 200:
                return await ctx.reply(":confused: Сервис не отвечает.")
            res = json.loads(await content.text())
            try:
                res['link']
            except:
                print(f"Error in:\n {content.text}\n\n")
                return await ctx.reply(":confused: Что-то пошло не так.")
            em = discord.Embed(color=0xa0cfe5)
            em.set_image(url=res['link'])
            await ctx.send("", embed=em)


async def nekoslifeapi(ctx, url: str):
    async with aiohttp.ClientSession() as session:            
        async with session.get(url) as content:
            if content.status != 200:
                return await ctx.reply(":confused: Сервис не отвечает.")
            res = json.loads(await content.text())
            try:
                res['url']
            except:
                print(f"Error in:\n {content.text}\n\n")
                return await ctx.reply(":confused: Что-то пошло не так.")
            em = discord.Embed(color=0xa0cfe5)
            em.set_image(url=res['url'])
            await ctx.send("", embed=em)