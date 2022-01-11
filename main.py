import os
import discord
import requests
import json
import datetime
import urllib
from keep_alive import keep_alive

help_info = [
    "**COMMANDS**\n\n'$inspire' TO GET RANDOM QUOTE\n\n'$date' TO GET CURRENT DATE\n\n'$ github search' TO SEARCH ACCOUNT ON GITHUB\n\n'$god'"
]
client = discord.Client()

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " \n-" + json_data[0]['a']
    return(quote)

def github_search_user(user_name):
        response = urllib.request.urlopen("https://api.github.com/users/" + user_name )
        data = json.loads(response.read())

        github_url = data["html_url"]
        repo = str(data["public_repos"])
        num_follower = str(data["followers"])
        num_following = str(data["following"])

        github_resource = [github_url,num_follower,num_following,repo]
        return github_resource

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

    if message.content.startswith('$date'):
        await message.channel.send(datetime.datetime.now())
    
    if message.content.startswith("$ github search"):
        user = message.content.split(" ",3)[3]
        github_result = github_search_user(user)
        await message.channel.send(github_result[0]+"\nFollowers:" + github_result[1]+"  Following:"+github_result[2]+"  Public_repo:"+github_result[3])
    
    if message.content.startswith("$get commands"):
        await message.channel.send(''.join(help_info))
    
    if message.content.startswith("$god"):
        await message.channel.send('We are here to help!')
    
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!')
    
token = os.environ.get("Token")
keep_alive()
client.run(token)
