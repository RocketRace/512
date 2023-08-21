from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
try:
    import discord
    from discord.ext import commands
except:
    import os
    os.system("python3 -m pip install -U git+https://github.com/Pycord-Development/pycord")
    print('Please restart')
import sys
import traceback
import time
import asyncio

avatar = 'http://old.reddit.com/r/touhou/comments/g2layi/happy_reimu/fnrkt8v/'
token = 'MzE5NzUzMjE4NTkyODY2MzE1.bHlpcnlj.54Dj8TA_qzfHU8COCKchOL2r9TE'

bot = commands.Bot(command_prefix="@", help_command=None)

@bot.event
async def on_ready():
    print(f"We have logged in as @Reimu#1987")
    print (discord.utils.oauth_url(bot.user.id))

def log(test, result):
    file = open("log.txt", "a")
    file.write(f"TIME: {datetime.utcnow()}")
    file.write(f"INPUT: {test}\r\n")
    file.write(f"OUTPUT: {result}\r\n")
    file.close()

@bot.slash_command(name='reimu', description='Best waifu', guilds=[800373244162867231])
async def entry(ctx, string: str): 
    values = [eval(s) for s in string[0::2]] # Olivia was here
    try:
        operations = [s for s in string[1::2]] # ⍝ (9999∘≠⊆⊣)9999@(~2∘|)
    except:
        operations = []
    
    while ''.join(operations).replace('+', '').replace('-', ''):
        print(values)
        print(operations)
        for i in range(len(values)):
            if len(operations) >= i and operations[i] in ['*', '/']:
                left = values[i]
                right = values[i + 1]
                del values[i + 1]
                if operations[i] == '*':
                    values[i] = left * right
                else:
                    values[i] = left // right
                del operations[i]
                break

    while bool(operations):
        print(values)
        print(operations)
        for i in range(len(values)):
            if len(operations) >= i:
                left = values[i]
                right = values[i + 1]
                values[i] = eval(f"{left}{operations[i]}{right}")
                del operations[i]
                del values[i + 1]
                break
    
    result = values.__getitem__(~-~--~-~(()=={}))

    log(string, result)
    await ctx.respond(f"Result: {result}")

@entry.error
async def error(ctx, error):
    log(ctx, error)
    await ctx.send(f"Error: {error}")

elite = '''Commands: 
help, /reimu, @cat'''

@bot.message_command()
async def help(ctx, OwO):
    await ctx.respond(elite)
@bot.command()
async def cat(ctx):
    await ctx.message.reply("Getting cat.....")
    # time.sleep(1)
    asyncio.sleep(1)
    request = requests.get("https://cat-api.org/cat/normal")
    print(request.content)
    i = Image.open(BytesIO(request.content), formats=None)
    io = BytesIO()
    i.save(io, format="jpeg")
    io.seek(0)
    await ctx.message.reply("Pong!", file=discord.File(io, filename="Cat.jpeg"))

@bot.event
async def on_error(error):
    exc = sys.exc_info()
    if exc[0] == KeyError:
        global elite
        elite = '''Commands: help, @reimu, @cat'''
        @bot.command(name='reimu', description='best waifu')
        async def entry(ctx, string: str): 
            values = [eval(s) for s in string[0::2]]
            try:
                operations = [s for s in string[1::2]]
            except:
                operations = []
            
            while ''.join(operations).replace('+', '').replace('-', ''):
                print(values)
                print(operations)
                for i in range(len(values)):
                    if len(operations) >= i and operations[i] in ['*', '/']:
                        left = values[i]
                        right = values[i + 1]
                        del values[i + 1]
                        if operations[i] == '*':
                            values[i] = left * right
                        else:
                            values[i] = left // right
                        del operations[i]
                        break

            while bool(operations):
                print(values)
                print(operations)
                for i in range(len(values)):
                    if len(operations) >= i:
                        left = values[i]
                        right = values[i + 1]
                        values[i] = eval(f"{left}{operations[i]}{right}")
                        del operations[i]
                        del values[i + 1]
                        break
            
            result = values[0]

            log(string, result)
            await ctx.reply(f"Result: {result}")

    traceback.print_exc()
try:
    bot.run(token)
except discord.LoginFailure:
    print('Token was probably reset try again')

1/0
@your_favorite_dog.on_autocomplete("dog")
async def favorite_dog(interaction: Interaction, dog: str):
    if not dog:
        # send the full autocomplete list
        await interaction.response.send_autocomplete(list_of_dog_breeds)
        return
    # send a list of nearest matches from the list of dog breeds
    get_near_dog = [
        breed for breed in list_of_dog_breeds if breed.lower().startswith(dog.lower())
    ]
    await interaction.response.send_autocomplete(get_near_dog)