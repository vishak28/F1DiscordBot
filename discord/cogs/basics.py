import discord
from discord.ext import commands
import json
import random

class basics(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is online')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'pong {round(self.bot.latency*1000)} ms')

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx):
        with open('./constants/_8ball.json') as _8ball_file: 
            _8ball = json.load(_8ball_file) 
        ans = random.choice(_8ball['responses'])['text']
        _8ball_file.close()
        await ctx.send(ctx.author.mention + ' ' + ans)
    
    @commands.command()
    async def choose(self, ctx, *, options):
        if '/' in options:
            choices = options.split('/')
        elif ' or ' in options:
            choices = options.split(' or ')
        else:
            await ctx.send('use "or" or "/"')
            return 
        await ctx.send(ctx.author.mention + ' ' + random.choice(choices) + ' :)')

def setup(bot):
    bot.add_cog(basics(bot))