import discord
from discord.ext import commands
import os, sqlite3

file = open("TOKEN.txt", "r")
line = file.readline()
file.close()

bot = commands.Bot(command_prefix='|', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("I`m on ready")

    global base, cur
    base = sqlite3.connect("Data.db")
    cur = base.cursor()
    if base:
        print("DataBase connected...Ok")


@bot.command()
async def test(ctx):
    await ctx.send("On place")


@bot.command()
async def info(ctx, arg=None):
    author = ctx.message.author
    if arg == None:
        await ctx.send(f'{author.mention}\nEnter:\n|info general\n|info commands\n|info rules')
    elif arg == 'general':
        await ctx.send(f'{author.mention}\nI`m - bot.I follow the order in the chat')
    elif arg == 'commands':
        await ctx.send(f'{author.mention}\n|test - is bot online?')
    elif arg == 'rules':
        await ctx.send(f'{author.mention}\nкороче, читы - бан, кемперство - бан, оскорбление - бан, оскорбление администрации - расстрел, потом бан')
    else:
        await ctx.send(f'{author.mention}\nNo such command')


bot.run(line)
