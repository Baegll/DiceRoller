# TODO: Restrict bot permissions
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

BOT_NAME = "DiceBot"

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

my_intents = discord.Intents.default()
my_intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=my_intents)


@bot.event
async def on_ready():
    print(f'{bot.user} is online.')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == 'testhello':
        await message.channel.send(f'Hey {message.author}')


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

bot.run(DISCORD_TOKEN)
