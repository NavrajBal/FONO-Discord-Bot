import discord

from secret import discordToken
from discord.ext import commands

print ("Hello World")

client = commands.Bot(command_prefix="=", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("IT WORKED!")

@client.command()
async def ping(ctx):
    await ctx.author.send("Pong!")

client.run(discordToken)
