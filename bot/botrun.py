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
async def info(ctx, *, arg):
    await ctx.send(arg)


bot.run(line)
