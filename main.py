import discord
import random
import pytz
from datetime import datetime
import asyncio
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO

last_gif = ''
last_replygif = ''
last_quote = ''
is_connected = False


TOKEN = ''
my_id = 334013974704029700
main_channel = 1076362742837022731
voice_channel = 1076362742837022732

randomgif_chance = 0.003
randomphrase_chance = 0.0066
timezone = pytz.timezone('Europe/Vilnius')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------') 
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print('------') 

    #send random gif on startup
    channel = bot.get_channel(main_channel)
    with open('static/text/gifs.txt', 'r') as file:
        gifs = file.readlines()
    gif = random.choice(gifs).strip()
    await channel.send(gif)
    print(f'Gif sent: {gif}')
    print('------') 




@bot.event
async def on_message(message):
    global last_gif
    global last_replygif
    global last_quote
    global is_connected

    if message.author == bot.user:
        return
    
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    #print(f'{username} in {channel}: {user_message}')       


    #reply to mentions
    if bot.user.mentioned_in(message) and random.random() < 0.3:
        with open('static/text/replygifs.txt', 'r') as file:
            replygifs = file.readlines()
        replygif = last_replygif
        while replygif == last_replygif:
            replygif = random.choice(replygifs).strip()

        last_replygif = replygif
        await message.reply(replygif)
        #LOG
        current_time = datetime.now(timezone)
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
        print(f'| {formatted_time} | Replying to {username} with gif')

    elif bot.user.mentioned_in(message):
        with open('static/text/patylekdegrade.txt', 'r') as file:
            patylekdegrade = file.readlines()
        await message.reply(random.choice(patylekdegrade).strip())
        #LOG
        current_time = datetime.now(timezone)
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
        print(f'| {formatted_time} | Replying to {username} with patylekdegrade')
        

    #if BOT got a private message send to me
    if message.channel.type == discord.ChannelType.private:
        user = await bot.fetch_user(my_id)
        await user.send(f'{username}: {user_message}')
        #LOG
        current_time = datetime.now(timezone)
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
        print(f'| {formatted_time} | PM: {username}: {user_message}')

    #if current time between 18 pm and 23 pm, connect to voice channel
    voice = discord.utils.get(bot.voice_clients, guild=message.guild)
    current_time = datetime.now(timezone)
    if (current_time.hour == 18 or current_time.hour == 19
            or current_time.hour == 20 or current_time.hour == 21
            or current_time.hour == 22 or current_time.hour == 23):
        if is_connected == False:   
            if voice is None:
        
                is_connected = True
                channel = bot.get_channel(voice_channel)
                await asyncio.sleep(random.randint(600, 10800))

                await channel.connect(self_mute=True, self_deaf=False)
                #LOG
                current_time = datetime.now(timezone)
                formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
                print(f'| {formatted_time} | Connected to VC')
            
    #if current time between 0 am and 11 am, disconnect from voice channel
    if (current_time.hour == 0 or current_time.hour == 1
            or current_time.hour == 2 or current_time.hour == 3
            or current_time.hour == 4 or current_time.hour == 5
            or current_time.hour == 6 or current_time.hour == 7
            or current_time.hour == 8 or current_time.hour == 9
            or current_time.hour == 10 or current_time.hour == 11):
        if is_connected == True:
            if voice is not None:
        
                is_connected = False
                await asyncio.sleep(random.randint(600, 7200))                     
                await voice.disconnect()
                #LOG
                current_time = datetime.now(timezone)
                formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
                print(f'| {formatted_time} | Disconnected from VC')
    
    #if current time between 13 pm and 17 pm, set is_connected to False
    if (current_time.hour == 13 or current_time.hour == 14
            or current_time.hour == 15 or current_time.hour == 16
            or current_time.hour == 17):
        if is_connected == True:
            is_connected = False

    
    #small chance to send gif or quote on message
    if random.random() < randomgif_chance and message.channel == bot.get_channel(main_channel):
        with open('static/text/gifs.txt', 'r') as file:
            gifs = file.readlines()

        gif = last_gif
        while gif == last_gif:
            gif = random.choice(gifs).strip()

        last_gif = gif
        #wait from 3 to 10 seconds
        await asyncio.sleep(random.randint(3, 60))
        await message.channel.send(gif)
        #LOG
        current_time = datetime.now(timezone)
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
        print(f'| {formatted_time} | {username} triggered gif')

    elif random.random() < randomphrase_chance and message.channel == bot.get_channel(main_channel):
        if random.random() < 0.3:
            with open('static/text/henrik_scraped.txt', 'r', encoding='utf-8', errors='ignore') as file:
                quotes = file.readlines()
            quote = last_quote
            while quote == last_quote:
                quote = random.choice(quotes).strip()
            last_quote = quote

            #wait from 3 to 10 seconds
            await asyncio.sleep(random.randint(3, 60))
            await message.channel.send(quote)
            #LOG
            current_time = datetime.now(timezone)
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
            print(f'| {formatted_time} | {username} triggered quote')
            
        else:
            with open('static/text/henrik_scraped.txt', 'r', encoding='utf-8', errors='ignore') as file:
                quotes = file.readlines()
            quote = last_quote
            while quote == last_quote:
                quote = random.choice(quotes).strip()
            last_quote = quote

            #wait from 3 to 10 seconds
            await asyncio.sleep(random.randint(3, 60))
            await message.reply(quote)
            #LOG
            current_time = datetime.now(timezone)
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
            print(f'| {formatted_time} | {username} triggered reply')
    
    
#neonoir command
@bot.tree.command(name="neonoir")
@app_commands.describe(user="Pasirinkite moteriškos lyties asmenį")
async def greet(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message("neo noir", ephemeral=True)
    await interaction.channel.send(f"{user.mention} <:aktyvuota:749638815445942302> turi kokiu nors underground neo-noir bangeriniu nuotrauku, ar dainu, ar kaip ir galvojau tiesiog front page scum normie material pas tave stalciuose?. Reik romance/old-school.  https://youtu.be/kPshx-3AFKo")
    #LOG user who used command
    current_time = datetime.now(timezone)
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
    print(f'| {formatted_time} | {interaction.user} used neonoir on {user}')

    

#post 1 random gif from gifs.txt
@bot.tree.command(name="henrikgif")
async def gif(interaction: discord.Interaction):
    global last_gif
    with open('static/text/gifs.txt', 'r') as file:
        gifs = file.readlines()

    gif = last_gif
    while gif == last_gif:
        gif = random.choice(gifs).strip()

    last_gif = gif
    await interaction.response.send_message(gif)
    #LOG
    current_time = datetime.now(timezone)
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
    print(f'| {formatted_time} | {interaction.user} used henrikgif')
    

#post 1 random phrase from static/henrik_scraped.txt, but not the last one
@bot.tree.command(name="henrikquote")
async def quote(interaction: discord.Interaction):
    global last_quote
    with open('static/text/henrik_scraped.txt', 'r', encoding='utf-8', errors='ignore') as file:
        quotes = file.readlines()

    quote = last_quote
    while quote == last_quote:
        quote = random.choice(quotes).strip()

    last_quote = quote
    await interaction.response.send_message(quote)
    #LOG
    current_time = datetime.now(timezone)
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
    print(f'| {formatted_time} | {interaction.user} used henrikquote')

#block command
@bot.tree.command(name="block")
@app_commands.describe(user="Išsirinkite degradą")
async def wanted(interaction: discord.Interaction, user: discord.Member):
    block = Image.open("static/images/block.png")
    block1 = Image.open("static/images/block1.png")
    block_mask = Image.open("static/images/block_mask.png")
    
    data = BytesIO(await user.display_avatar.read())
    pfp = Image.open(data)

    pfp = pfp.resize((54, 54))

    block.paste(pfp, (56, 53))
    block.paste(block1, (0, 0), mask=block_mask)

    block.save("static/images/image.png")

    file = discord.File("static/images/image.png", filename="image.png")
    await interaction.response.send_message("blocked", ephemeral=True)
    await interaction.channel.send(file=file)
    #LOG user who used command
    current_time = datetime.now(timezone)
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
    print(f'| {formatted_time} | {interaction.user} used block on {user}')



bot.run(TOKEN)


