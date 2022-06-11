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
flatmates = ["Emily","Simran","Ojaswee"]

async def mentioning_User():
  flatBotChannel = client.get_channel(634765417574957078)
  user = discord.utils.get(client.users, name="waterbottle", discriminator=8767)
  if user is None:
      print("User not found")
  else:
      await flatBotChannel.send(f"{user.mention} is the best")

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
    await mentioning_User()

    

# def runBot():
#   client.on("ready", testChannel())

async def printSchedule():
  global flatmates  

  results = collection.find({"_id":0})
  numArr = [result["num"] for result in results]
  num = numArr[0]

  flatBotChannel = client.get_channel(634765417574957078)
  
  await flatBotChannel.send("Hiiiii! This week it is "+ flatmates[num % 3] + "'s turn to take out the kitchen bins and vacuum/broom the corridor & floors.")

  await flatBotChannel.send(flatmates[(num+1) % 3] + "'s turn to clean the toilet and shower - wipe down surfaces, clean the shower :)) ")

  await flatBotChannel.send(flatmates[(num+2) % 3] + "'s turn to clean the kitchen. This includes cleaning the surfaces, the hob, the microwave (inside too), the fridge (inside as well).")

  update_num()

# @aiocron.crontab('0 0 * * mon,wed,fri,sun')
@aiocron.crontab('0 0 * * mon')
async def cornjob1():
    await printSchedule()

client.run(TOKEN)

