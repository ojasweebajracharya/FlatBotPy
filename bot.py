import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print("Bot is ready!")


# test
async def on_message(message):
    if message.author.bot:
        return
    else:
        await message.channel.send("Hello there!")
    
    
client.run(os.environ['TOKEN'])
