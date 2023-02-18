import discord
import random


last_gif = ''
last_replygif = ''

TOKEN = 'MTA3NjM2ODMxMDI3NjQ2ODc0Ng.Gqv8TD.VsXGj7_OjI7RGSgZMKps8WxUzDE23iq9wgvKr8'
main_channel = 1076362742837022731
reply_chance = 2


def run_discord_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)


    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        channel = client.get_channel(main_channel)

        with open('static/gifs.txt', 'r') as file:
            gifs = file.readlines()
    
        gif = random.choice(gifs).strip()
        await channel.send(gif)

    #when user types 'gif' in chat, bot sends random gif from static/gifs.txt
    @client.event
    async def on_message(message):
        global last_gif
        global last_replygif

        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} in {channel}: {user_message}')       

        if message.content.startswith('gif'):
            with open('static/gifs.txt', 'r') as file:
                gifs = file.readlines()

            gif = last_gif
            while gif == last_gif:
                gif = random.choice(gifs).strip()

            last_gif = gif
            await message.channel.send(gif)

        #if message contains "henrik" somewhere inside it, bot sends random gif from static/gifs.txt
        if 'henrik' in message.content.lower() and random.random() < reply_chance:
            with open('static/replygifs.txt', 'r') as file:
                replygifs = file.readlines()

            replygif = last_replygif
            while replygif == last_replygif:
                replygif = random.choice(replygifs).strip()

            last_replygif = replygif
            await message.reply(replygif)

    client.run(TOKEN)
