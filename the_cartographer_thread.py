import sys, os, time, re
import requests, json
import queue
import threading

import discord

client = discord.Client()
token = ''

headers = {
    'origin': 'https://discordapp.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'fr',
    'authorization': token,
    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMC4yOTgiLCJvc192ZXJzaW9uIjoiMTAuMC4xNDM5MyJ9',
    'cookie': 'locale=us;',
    'content-length': '0',
    'pragma': 'no-cache',
    'x-context-properties': 'eyJsb2NhdGlvbiI6Ikludml0ZSBCdXR0b24gRW1iZWQifQo=',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.9 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36',
    'accept': '*/*',
    'cache-control': 'no-cache',
    'authority': 'discordapp.com',
    'referer': 'https://discordapp.com/channels/@me',
}


@client.event
async def on_ready():
    print("primed and ready")

def random_proxy():
    with open("proxy.txt") as f:
        return random.choice(f.readlines())

def join_discords():
    while(True):
        if queue:
            discord = queue.pop()
            print("join_discords -> joining", discord)
            response = requests.post('https://discordapp.com/api/v6/invites/' + discord.split("/")[-1], headers=headers)
            if response.status_code == 429:
                print("join_discords -> Rate limit hit waiting a minute")
                time.sleep(random.randint(120,180))
                queue.add(discord)
            elif not response.ok:
                print("join_discords -> Invite down")
        time.sleep(random.randint(30,60))

@client.event
async def on_guild_join(guild):
    print("on_guild_join -> joined", guild)
    for channel in list(guild.text_channels):
        try:
            async for message in channel.history(limit=None, oldest_first=True):
                invit = re.search('discord(.gg|app.com/invite)/[0-9A-Za-z]{3,15}', str(message.content))
                if invit is not None and invit not in total_invits:
                    queue.add(invit.group())
                    total_invits.add(invit.group())
                    print("on_guild_join -> added to queue", invit.group(), "Invites pending", len(queue), "Total invites", len(total_invits))
        except Exception as e:
            print("on_guild_join -> Fkn 50001")

@client.event
async def on_message(message):
    try: print(message.channel.name, message.author, message.content)
    except: pass
    
    invit = re.search('discord(.gg|app.com/invite)/[0-9A-Za-z]{3,15}', str(message.content))
    if invit is not None and invit not in total_invits: 
        queue.add(invit.group())
        total_invits.add(invit.group())
        print("on_message -> added to queue", invit.group(), "Invites pending", len(queue), "Total invites", len(total_invits))

if __name__ == '__main__':
    queue          = set()
    total_invits   = set()

    j = threading.Thread(name = "join_discords", target=join_discords)
    j.start()
    print("Starting join thread") 

    print("Starting client thread") 
    client.run(token, bot=False)