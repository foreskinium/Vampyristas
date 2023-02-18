import discord
import random
import pytz
from datetime import datetime
import asyncio


last_gif = ''
last_replygif = ''

TOKEN = ''
my_id = 334013974704029700
main_channel = 1076362742837022731
voice_channel = 1076362742837022732

replygif_chance = 0.4
patylekdegrade_chance = 0.3
randomgif_chance = 0.004
connect_chance = 0.01
timezone = pytz.timezone('Europe/Vilnius')


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

  

        #send random gif on startup
        channel = client.get_channel(main_channel)
        with open('static/gifs.txt', 'r') as file:
            gifs = file.readlines()
    
        gif = random.choice(gifs).strip()
        await channel.send(gif)
        print(f'Gif sent: {gif}')



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

        #maybe send gif on message
        if random.random() < randomgif_chance:
            with open('static/gifs.txt', 'r') as file:
                gifs = file.readlines()

            gif = last_gif
            while gif == last_gif:
                gif = random.choice(gifs).strip()

            last_gif = gif
            await asyncio.sleep(random.randint(1, 5))
            await message.channel.send(gif) 

        current_time = datetime.now(timezone)
        #if current_time.hour from 18 to 23
        if (current_time.hour == 18 or current_time.hour == 19
             or current_time.hour == 20 or current_time.hour == 21
               or current_time.hour == 22 or current_time.hour == 23) and random.random() < connect_chance:
        
                channel = client.get_channel(voice_channel)
                #try connect if error print "already in voice"
                try:
                    await channel.connect(self_mute=True, self_deaf=False)
                    print('Connected to voice')
                except:
                    print('ERROR: Already in voice')

        #if time is 02 am
        if current_time.hour == 2:
            #try disconnect if error print "not in voice"
            try:     
                await asyncio.sleep(random.randint(300, 1800))
                for vc in client.voice_clients:
                    if vc.guild == message.guild:
                        await vc.disconnect()
                        print('Disconnected from voice')
            except:
                print('ERROR: Not in voice')
        
        #if message contains "henrik" somewhere inside it, bot sends random gif from static/replygifs.txt
        if 'henrik' in message.content.lower() and random.random() < replygif_chance:
            with open('static/replygifs.txt', 'r') as file:
                replygifs = file.readlines()

            replygif = last_replygif
            while replygif == last_replygif:
                replygif = random.choice(replygifs).strip()

            last_replygif = replygif
            await asyncio.sleep(random.randint(5, 15))
            await message.reply(replygif)
        elif 'henrik' in message.content.lower() and random.random() < patylekdegrade_chance:
            await asyncio.sleep(random.randint(3, 6))
            await message.reply('patylek degrade') 

        #if BOT got a private message send to me
        if message.channel.type == discord.ChannelType.private:
            user = await client.fetch_user(my_id)
            await user.send(f'{username}: {user_message}')



    client.run(TOKEN)

