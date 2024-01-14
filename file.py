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

@client.command()
async def count(ctx):
    await ctx.channel.send(ctx.channel)

@client.command()
async def channels(ctx):
    dServer = ctx.guild
    allChannels = ctx.guild.channels 

    vcList = []

    for c in allChannels:
        if c.type == discord.ChannelType.voice:
            vcList.append(c.name)
        pass


    await ctx.channel.send(vcList)



client.run(discordToken)
