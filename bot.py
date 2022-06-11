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
oj_id = "571276422363217951"
em_id = "238389040187965441"
sim_id = "719261320662351950"
flatmates_ids = [em_id, sim_id, oj_id]

# async def mentioning_User():
#   flatBotChannel = client.get_channel(634765417574957078)
#   print(client.users)
#   oj_id = "571276422363217951"
#   em_id = "238389040187965441"
#   sim_id = "719261320662351950"
#   await flatBotChannel.send(f"<@{oj_id}> is the best")

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
  global flatmates_ids  

  results = collection.find({"_id":0})
  numArr = [result["num"] for result in results]
  num = numArr[0]

  flatBotChannel = client.get_channel(634765417574957078)
  
  await flatBotChannel.send(f"Hiiiii! This week it is <@{flatmates_ids[num % 3]}>'s turn to take out the kitchen bins and vacuum/broom the hall")

  await flatBotChannel.send(f"<@{flatmates_ids[(num+1) % 3]}>'s turn to clean the toilet and shower - wipe down surfaces, clean the floor, clean the shower :)) ")

  await flatBotChannel.send(f"<@{flatmates_ids[(num+2) % 3]}>'s turn to clean the kitchen. This includes cleaning the surfaces, sweep the floor and use floor wipes for any spillss etc. clean the hob, the microwave (inside too), the fridge (inside as well).")

  update_num()

@aiocron.crontab('0 0 * * mon')
async def cornjob1():
    await printSchedule()



# @aiocron.crontab('0 0 * * mon,wed,fri,sun')
# @aiocron.crontab('0 0 * * mon')
# async def cornjob1():
#     await printSchedule()

client.run(TOKEN)

