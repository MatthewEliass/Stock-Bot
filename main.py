# main.py
import os
import discord
import random
import requests
import datetime

from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Gives the bot access to Guild member and message information
intents = discord.Intents.default()
intents.members = True
intents.messages = True

# Loads token/guild info from env file
load_dotenv('.env.py')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Loads current time
now = datetime.datetime.now()
current_hour = now.strftime('%H')
current_min = now.strftime('%M')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('bot is ready')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Ready to find Stocks!"))

@bot.event
async def on_member_join(member):
    await bot.get_channel(796154565581209621).send(f'{member.mention} welcome to the server!')
    print(f'{member.name} has connected')

@bot.command(name='respond')
async def respond(ctx):
    quotes = ['What do you need?', 'Why did you summon me?', 'How can I help you?']
    response = random.choice(quotes)
    respondto = ctx.message.author.mention
    await ctx.send('Hi! ' + respondto + ' ' + response)

@bot.command(name='stock')
async def stock(ctx, arg):
    yahoo = 'https://finance.yahoo.com/quote/'
    url = yahoo + arg
    parse = requests.get(url)
    soup = BeautifulSoup(parse.content, 'html.parser')
    stock_price = soup.find_all(class_= 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')[0].text

    await ctx.send(ctx.message.author.mention + ' ' + arg.upper() + ' is currently trading at ' + '$' + stock_price)




bot.run(TOKEN)