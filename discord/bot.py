import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix = '#')

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run('NzM3NzQ5MTQzMDY5NTI0MTQz.XyB4bg.8iK_CU6sINYB214LSGVmjWj4FUw')