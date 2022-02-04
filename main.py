#imports
from discord.ext import tasks,commands
import random
import datetime
import urllib
import discord 
import requests
import json

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.guilds = True

client = commands.Bot(command_prefix="$",intents=intents)

#variables
games = ["GTA V","VALORENT","GOD OF WAR","HALO INFINITE","CALL OF DUTY VANGUARD"]
help_info = [
    "**COMMANDS**\n\n'inspire' TO GET RANDOM QUOTE\n\n'date?' TO GET CURRENT DATE\n\n'$github' TO SEARCH ACCOUNT ON GITHUB\n\n'joke' TO GET RANDOM JOKE\n\n'$clear' TO CLEAR MESSAGE "
]

#function to get random quote
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")#random api to get a random quote
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " \n-" + json_data[0]['a']
    return(quote)

#function to return github account 
def github_search_user(user_name):
        response = urllib.request.urlopen("https://api.github.com/users/" + user_name )
        data = json.loads(response.read())

        github_url = data["html_url"]
        repo = str(data["public_repos"])
        num_follower = str(data["followers"])
        num_following = str(data["following"])

        github_resource = [github_url,num_follower,num_following,repo]
        return github_resource

#function to return random joke
def random_joke():
    url = "https://some-random-api.ml/joke"
    responce = urllib.request.urlopen(url)
    data = json.loads(responce.read())
    joke = data["joke"]
    return joke

#function to retun random joke
def random_meme():
    url = "https://some-random-api.ml/meme"
    responce = urllib.request.urlopen(url)
    data = json.loads(responce.read())
    meme = data["image"]
    return meme

#created login message
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    await client.wait_until_ready()
    bot_status.start()
    print("Bot is ready!!")

#task is looped which change the status of bot frequently
@tasks.loop(seconds=60)
async def bot_status(): 
    await client.change_presence(activity=discord.Game(random.choice(games)))

#gives welcome message when someone joins the server
@client.event
async def on_member_join(member):
    channel = client.get_channel(880848956282781787)    
    embed=discord.Embed(title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!")
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)

#gives good bye message when someone leaves the server
@client.event
async def on_member_remove(member):
    channel = client.get_channel(880848956282781787)
    embed=discord.Embed(title=f"Good bye {member.name}!!", description=f"I was such a pleasure to meet you :pray: ")
    await channel.send(embed = embed)


@client.listen()
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

#condition to return random Quotes
    if message.content.startswith('get a quote'):
        quote = get_quote()
        await message.channel.send(quote)

    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

#condition requesting current date-time
    if message.content.startswith('date'):
        await message.channel.send(datetime.datetime.now())
    
#condition to return random jokes
    if message.content.startswith("joke"):
        joke = random_joke()
        await message.channel.send('>>> '+joke)
 
 #condition to return random meme 
    if message.content.startswith("meme"):
        meme = random_meme()
        await message.channel.send(meme)
        
 #condition to return linktree
    if message.content.startswith('Linktree'):
        await message.channel.send('Hello '+str(message.author)+' !'+'\n'+'You can look up my linktree @: '+'https://dot-space.github.io/dot-linktree/')
        
 #condition to return github
    if message.content.startswith('Github'):
        await message.channel.send('Hello '+str(message.author)+' !'+'\n'+'You can look up my github @: '+'https://github.com/dot-space')

#command to send command info
@client.command()
async def commands(ctx):
    await ctx.send(''.join(help_info))

#command to send 
@client.command()
async def github(ctx,member):
    github_result = github_search_user(member)
    await ctx.send(github_result[0]+"\nFollowers:" + github_result[1]+"  Following:"+github_result[2]+"  Public_repo:"+github_result[3])

#command to clear messages 
@client.command()
async def clear(ctx,amount):
    amt = int(amount)+1
    await ctx.channel.purge(limit = amt)

#command to kick member
@client.command()
async def kick(ctx,member:discord.Member,*,reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention} \n\nReason: {reason}")

#command to ban member
@client.command()
async def ban(ctx,member:discord.Member,*,reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")

#command DM invite link to member
@client.command(pass_context=True )
async def DM(ctx, user: discord.Member):
    link = await ctx.channel.create_invite(max_use = 2)
    await ctx.send("invite sent")
    await user.send(link)

#command to unban member
@client.command()
async def unban(ctx,*,member):
    banned_user = await ctx.guild.bans()
    member_name, member_disc = member.split("#")

    for ban_entry in banned_user:
        user = ban_entry.user

        if(user.name , user.discriminator) == (member_name,member_disc):
            
            await ctx.guild.unban(user)
            await ctx.send(f"unban {user.mention}#{user.discriminator}")
                                                    
            # await asyncio.gather(DM(ctx,user))
            
        return

Token = "Your TOKEN"
client.run(Token)
