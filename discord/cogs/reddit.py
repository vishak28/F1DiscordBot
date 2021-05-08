import discord
from discord.ext import commands
import praw

r = praw.Reddit(client_id = 'WuABUBCKzMNqSw',
                    client_secret = 'YWNWQfrbm9Gk3owZwESmBuZsjmE',
                    username = 'xxxdog6969',
                    password = 'ph9035249775', 
                    user_agent = 'edgybot')


class reddit(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def r(self, ctx, sub, start=1, i=1):
        i = int(i)
        start = int(start)
        try:
            subreddit = r.subreddit(sub)
            hot = list(subreddit.hot(limit = i+start-1))[start-1: start-1+i]
            for post in hot:
                embed = discord.Embed(
                    title = post.title,
                    colour = 0xff4301,
                    url = post.url
                )
                embed.set_author(
                    name = 'r/'+sub,
                    url = 'https://reddit.com/r/'+sub, 
                    icon_url = "https://cdn0.iconfinder.com/data/icons/most-usable-logos/120/Reddit-512.png"                
                )
                if post.url[-3:] in ['jpg','png']:
                    embed.set_image(url = post.url) 
                else:
                    embed.description = '[POST] ' + post.url 
                embed.set_footer(text = '👍' + str(post.score))     
                await ctx.send(embed = embed)
        except:
            await ctx.send('subreddit doesn\'t exist')

def setup(bot):
    bot.add_cog(reddit(bot))