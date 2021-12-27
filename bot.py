import discord
import os
import aiocron
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
client = discord.Client()
flatBotChannel = client.get_channel(634765417574957078)
num = 0
flatmates = ["Simran","Ojaswee","Emily","Fraser"]

# @client.event
# async def on_ready():
#     print("Bot is ready!")


# test
# @client.event
# async def on_message(message):
#     if message.author.bot:
#         return
#     else:
#         await message.channel.send("Hello there!")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    

# def runBot():
#   client.on("ready", testChannel())

async def printSchedule():
  global num
  global flatmates  
  flatBotChannel = client.get_channel(634765417574957078)
  
  await flatBotChannel.send("Hiiiii! This week it is "+ flatmates[num % 4] + "'s turn to take out the kitchen bins and vacuum the corridor and mop (if needed). ")

  await flatBotChannel.send(flatmates[(num+1) % 4] + "'s turn to clean the bathroom with the shower (clean shower, wipe all surfaces, mop floor? (vacuum? if the floor is dry?))")

  await flatBotChannel.send(flatmates[(num+2) % 4] + "'s turn to clean the smaller bathroom - clean all surfaces, mop floor? vacuum?")

  await flatBotChannel.send(flatmates[(num+3) % 4] + "'s turn to clean the kitchen and sofa areas. This includes vacuuming the floor, mopping, cleaning all surfaces which includes sink, hob, fridge etc.")

  num += 1

@aiocron.crontab('0 0 * * tue,thu,sat')
async def cornjob1():
    await printSchedule()

client.run(TOKEN)

