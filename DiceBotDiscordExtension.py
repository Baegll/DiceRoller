# TODO: Restrict bot permissions
import discord
import DiceRoller

import os
from dotenv import load_dotenv

BOT_NAME = "DiceBot"

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="singlestat")
async def singlestat(ctx):
    full_value = DiceRoller.dice_roller("4d6l1")
    stat_value = DiceRoller.stat_definer(full_value[0])
    await ctx.respond(f"Stat value: {full_value[0]}, {stat_value}\nRolls: {full_value[1]}")


bot.run(DISCORD_TOKEN)
