import discord
from discord.ext import commands
import requests

class emotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def e(self, ctx, emote):
        try:
            payload = {'q': f'{emote}', 'sort':'count-desc'}
            x = requests.get('https://api.frankerfacez.com/v1/emoticons?_sceheme=https', params=payload)
            x = x.json()
            embed = discord.Embed(
                    colour = 0x2C2F33,
                )
            embed.set_author(
                name = ctx.author.display_name + ':',
                icon_url = ctx.author.avatar_url
            )
            embed.set_thumbnail(url = 'https:'+ x['emoticons'][0]['urls']['1'])
            try:
                await ctx.channel.purge(limit = 1)
            except:
                pass
            await ctx.send(embed = embed)
        except:
            await ctx.send(emote + ' doesn\'t exist')

def setup(bot):
    bot.add_cog(emotes(bot))