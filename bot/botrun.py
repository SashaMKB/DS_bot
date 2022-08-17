import discord
from discord.ext import commands
import os

file = open("TOKEN.txt", "r")
line = file.readline()
file.close()

bot = commands.Bot(command_prefix='|')

bot.run(line)
