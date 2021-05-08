import discord
import pymongo
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://botAdmin:bot123@cluster0.byvp4.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['discordBot']
collection = db['dB']

class database(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        _id = collection.find_one({'_id': ctx.author.id})
        if _id != None:
            await ctx.send('User already joined')
            return
        data = {'_id': ctx.author.id, 'name': ctx.author.name, 'gold': 1000, 'todo_list':[]}
        collection.insert_one(data)

    @commands.command()
    async def gold(self, ctx):
        _id = collection.find_one({'_id': ctx.author.id})
        if _id == None:
            await ctx.send('No data found, use \'#join\' to register')
            return
        await ctx.send(ctx.author.mention + ' has ' + str(_id['gold']) + ' gold')

########################################### Todo ################################################

    @commands.command()
    async def todo(self, ctx):
        _id = collection.find_one({'_id': ctx.author.id})
        if _id == None:
            await ctx.send('No data found, use \'#join\' to register')
            return

        if len(_id['todo_list']) == 0:
            await ctx.send('List is empty')
            return

        res = ctx.author.mention + ' \'s To-do List:\n'
        for i,item in enumerate(_id['todo_list'], start = 1):
            res += str(i) + ') '
            if item['done']:
                res += '~~' + item['message'] + '~~ \n'
            else:
                res += item['message'] + '\n'      
        await ctx.send(res)

    @commands.command()
    async def add_todo(self, ctx, *, message):
        _id = collection.find_one({'_id': ctx.author.id})
        if _id == None:
            await ctx.send('No entry found, use \'#join\' to make one')
            return
        collection.update_one({'_id': ctx.author.id}, {'$push': {'todo_list': {'message': message, 'done': False}}})

    @commands.command()
    async def remove_todo(self, ctx, i):
        i = int(i)
        item = collection.find_one({'_id': ctx.author.id})
        if item == None:
            await ctx.send('No entry found, use \'#join\' to make one')
            return
        if len(item['todo_list']) < i:
            await ctx.send('Out of index')
            return
        m = item['todo_list'][i-1]['message']
        collection.update_one({'_id': ctx.author.id}, {'$pull': {'todo_list': {'message' : m}}})

###################################################################################################
def setup(bot):
    bot.add_cog(database(bot))