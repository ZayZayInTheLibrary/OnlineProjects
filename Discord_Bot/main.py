import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
load_dotenv()

token = os.getenv('DISC_TOKEN')


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(str(token))