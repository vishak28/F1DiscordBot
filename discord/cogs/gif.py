import discord
import urllib.request
from discord.ext import commands

class gif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mg(self, ctx, file):
        extension = file[-5:].split('.')[-1]
        # urllib.request.urlretrieve(file, "images/imgname.jpeg" + extension)
        await ctx.send(file)

def setup(bot):
    bot.add_cog(gif(bot))