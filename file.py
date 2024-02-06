import discord

from secret import discordToken
from discord.ext import commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

class settings:
    def __init__(self, id) -> None:
        self.id = id
        self.isFollowing = False
        self.minSzie = 2
        self.followingSize = 0
        self.following = []
        self.delay = 10
        self.conditionMet = False


userPrefs = {}

# connection test
@client.event
async def on_ready():
    print("IT WORKED!")


# init user preferences
@client.command()
async def init(ctx):
    id = ctx.author.id
    
    if (id not in userPrefs):
        userPrefs[id] = settings(id)
        await ctx.channel.send(ctx.author)
    else:
        await ctx.channel.send("you are already setup")

# add followers
@client.command()
async def add(ctx):
    id = ctx.author.id

    if (id not in userPrefs):
        await ctx.channel.send("You are not setup. Try !init then add")
    else:
        mentionsList = ctx.message.mentions
        for i in mentionsList:
            userPrefs[id].following.append(i)
            userPrefs[id].followingSize += 1
            
        userPrefs[id].isFollowing = True if userPrefs[id].followingSize >= 1 else False
        await ctx.channel.send(userPrefs[id].following)

# remove followers
@client.command()
async def remove(ctx):
    id = ctx.author.id

    if (id not in userPrefs):
        await ctx.channel.send("You are not setup. Try !init then add")
    elif (userPrefs[id].followingSize == 0):
        await ctx.channel.send("You are not following anyone")
    else:
        mentionsList = ctx.message.mentions
        for i in mentionsList:
            userPrefs[id].following.remove(i)
            userPrefs[id].followingSize -= 1
        
        userPrefs[id].isFollowing = True if len(userPrefs[id].following) >= 1 else False
        await ctx.channel.send(userPrefs[id].following)

# output vc with participants
@client.command()
async def channels(ctx):
    dServer = ctx.guild
    allChannels = ctx.guild.channels 

    vcList = []
    vcDict = {}

    for c in allChannels:
        if c.type == discord.ChannelType.voice:
            vcList.append(c.id)

            vcDict[c.id] = 0

            for memb in c.members:
                vcDict[c.id] += 1
                await ctx.channel.send(memb)

    await ctx.channel.send(vcDict)

# output all following
@client.command()
async def following(ctx):
    id = ctx.author.id
    for i in userPrefs[id].following:
        await ctx.channel.send(userPrefs[id].following)

# dm if a follower joined vc
@client.event
async def on_voice_state_update(member, before, after):
    for user in userPrefs:
        if member in userPrefs[user].following:
            if before.channel is None and after.channel is not None:
                userPrefs[user].conditionMet = True
                await member.send(member.name + " is in a vc.")


client.run(discordToken)

