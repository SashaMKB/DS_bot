import discord
from discord.ext import commands
import os, sqlite3
import string
import json

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
        await ctx.send(
            f'{author.mention}\nкороче, читы - бан, кемперство - бан, оскорбление - бан, оскорбление администрации - расстрел, потом бан')
    else:
        await ctx.send(f'{author.mention}\nNo such command')


@bot.event
async def on_message(message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) \
    for i in message.content.split(' ')}.intersection(set(json.load(open('cenz.json')))) != set():  # "whats up" in message.content.lower():
        await message.channel.send(f'{message.author.mention},you say banned word')
        await message.delete()

    await bot.process_commands(message)

@bot.command()
async def send(ctx):
    await ctx.author.send('Hello World')

@bot.command()
async def send_member(ctx, member:discord.Member):
    await member.send(f'{member.name}, hi from {ctx.author.name}')

@bot.command()
async def clear(ctx, amount=100):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount)




bot.run(line)
