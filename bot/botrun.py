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

        name = message.guild.name
        base.execute('CREATE TABLE IF NOT EXISTS warning(userid INT, count INT)')
        base.commit()

        warnings = cur.execute('SELECT * FROM warning WHERE userid == ?', (message.author.id,)).fetchone()

        if warnings is None:
            cur.execute('INSERT INTO warning VALUES(?, ?)',(message.author.id, 1))
            base.commit()
            await message.channel.send(f'{message.author.mention}, First warning, maximum amount - 3.')
        elif warnings[1] == 1:
            cur.execute('UPDATE warning SET count == ? WHERE userid == ?', (2, message.author.id))
            base.commit()
            await message.channel.send(f'{message.author.mention}, Second  warning, maximum amount - 3.')
        elif warnings[1] == 2:
            await message.channel.send(f'{message.author.mention}, Wasted...')
            cur.execute('UPDATE warning SET count == ? WHERE userid == ?', (3,message.author.id))
            base.commit()
            await message.channel.send(f'{message.author.mention}, banned for no reason')
            await message.author.ban(reason='This server for cool guys')

    await bot.process_commands(message)

@bot.command()
async def status(ctx, member: discord.Member):
    base.execute('CREATE TABLE IF NOT EXISTS warning(userid INT, count INT)')
    base.commit()
    warnings = cur.execute('SELECT * FROM warning WHERE userid == ?', (member.id,)).fetchone()
    if warnings == None:
        await ctx.send(f'{ctx.message.author.mention}, clear yet')
    else:
        await ctx.send(f'{ctx.message.author.mention}, Gotcha, you have  {warnings[1]} warnings')
@bot.command()
async def send(ctx):
    await ctx.author.send('Hello World')

@bot.command()
async def send_member(ctx, member: discord.Member):
    await member.send(f'{member.name}, hi from {ctx.author.name}')

@bot.command()
async def clear(ctx, amount=100):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount)

@bot.event
async def on_member_join(member):
    await member.send('Welcome home, good hunter')
    for ch in bot.get_guild(member.guild.id).text_channels:
        await bot.get_channel(ch.id).send(f'{member.name}, what is it your desire?')

@bot.event
async def on_member_remove(member):
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, I will wait for you')
bot.run(line)
