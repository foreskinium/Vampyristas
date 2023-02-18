import discord
import random
import time


last_gif = ''
last_replygif = ''

TOKEN = 'MTA3NjM2ODMxMDI3NjQ2ODc0Ng.Gqv8TD.VsXGj7_OjI7RGSgZMKps8WxUzDE23iq9wgvKr8'
my_id = 334013974704029700
main_channel = 1076362742837022731
replygif_chance = 0.5
patylekdegrade_chance = 0.3
randomgif_chance = 0.004


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

        ####################################################################
        #send random gif on startup #########################################
        ####################################################################
        with open('static/gifs.txt', 'r') as file:
            gifs = file.readlines()
    
        gif = random.choice(gifs).strip()
        await channel.send(gif)
        ####################################################################


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

        ####################################################################
        #maybe send gif on message
        ####################################################################
        if random.random() < randomgif_chance:
            with open('static/gifs.txt', 'r') as file:
                gifs = file.readlines()

            gif = last_gif
            while gif == last_gif:
                gif = random.choice(gifs).strip()

            last_gif = gif
            time.sleep(random.randint(1, 5))
            await message.channel.send(gif)
        ####################################################################        
        
        ####################################################################
        #if message contains "henrik" somewhere inside it, bot sends random gif from static/replygifs.txt
        ####################################################################
        if 'henrik' in message.content.lower() and random.random() < replygif_chance:
            with open('static/replygifs.txt', 'r') as file:
                replygifs = file.readlines()

            replygif = last_replygif
            while replygif == last_replygif:
                replygif = random.choice(replygifs).strip()

            last_replygif = replygif
            time.sleep(random.randint(5, 15))
            await message.reply(replygif)
        elif 'henrik' in message.content.lower() and random.random() < patylekdegrade_chance:
            time.sleep(random.randint(3, 6))
            await message.reply('patylek degrade') 
        ####################################################################

        ####################################################################
        #if BOT got a private message send to me
        ####################################################################
        if message.channel.type == discord.ChannelType.private:
            user = await client.fetch_user(334013974704029700)
            await user.send(f'{username}: {user_message}')

        ####################################################################

    client.run(TOKEN)
