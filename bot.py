import discord
import os
import aiocron
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient

# Connecting to MongoDB
MONGO_URI = os.getenv('MONGO_URI')
cluster = MongoClient(MONGO_URI)
db = cluster["discord"]
collection = db["globalvars"]

# check if "num" exists in the collection


# post = {"_id":0, "num": 0}
# collection.insert_one(post)

load_dotenv()
TOKEN = os.getenv('TOKEN')
client = discord.Client()
flatmates = ["Simran","Ojaswee","Emily","Fraser"]

def update_num():
  collection.update_one({"_id":0},{ "$inc": {"num": +1}})

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
  global flatmates  

  results = collection.find({"_id":0})
  num = [result["num"] for result in results]
  print("num: " + num)

  flatBotChannel = client.get_channel(634765417574957078)
  
  await flatBotChannel.send("Hiiiii! This week it is "+ flatmates[num % 4] + "'s turn to take out the kitchen bins and vacuum the corridor and mop (if needed). ")

  await flatBotChannel.send(flatmates[(num+1) % 4] + "'s turn to clean the bathroom with the shower (clean shower, wipe all surfaces, mop floor? (vacuum? if the floor is dry?))")

  await flatBotChannel.send(flatmates[(num+2) % 4] + "'s turn to clean the smaller bathroom - clean all surfaces, mop floor? vacuum?")

  await flatBotChannel.send(flatmates[(num+3) % 4] + "'s turn to clean the kitchen and sofa areas. This includes vacuuming the floor, mopping, cleaning all surfaces which includes sink, hob, fridge etc.")

  update_num()

# @aiocron.crontab('0 0 * * mon,wed,fri,sun')
@aiocron.crontab('*/1 * * * *')
async def cornjob1():
    await printSchedule()

client.run(TOKEN)

