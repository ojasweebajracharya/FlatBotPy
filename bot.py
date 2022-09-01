import discord
import os
import aiocron
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import logging
import gspread

logging.basicConfig(level=logging.INFO)

# Connecting to MongoDB
MONGO_URI = os.getenv('MONGO_URI')
cluster = MongoClient(MONGO_URI)
db = cluster["discord"]
collection = db["globalvars"]

# check if "num" exists in the collection

# post = {"_id":0, "num": 0}
# collection.insert_one(post)


intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('TOKEN')
client = discord.Client(intents=intents)
oj_id = "571276422363217951"
em_id = "238389040187965441"
sim_id = "719261320662351950"
flatmates_ids = [em_id, sim_id, oj_id]

spreadsheet_id = "1iPj_UJp5D-LJJFSppaZTyJEqQvPjMi2YUPMN7c3-tbg"
sheet_id = 0
sa = gspread.service_account(filename="service_account.json")
sh = sa.open("Money")
wks = sh.worksheet("Monthly")

def update_num():
  collection.update_one({"_id":0},{ "$inc": {"num": +1}})

# @client.event
# async def on_ready():
#     print("Bot is ready!")


# test
@client.event
async def on_message(message):
    global wks
    if message.author.bot:
        return
    else:
        await message.channel.send("Hello there!")
        await message.channel.send(wks.acell('Y3:Z3').value)
        await message.channel.send(wks.acell('Y4:Z4').value)
        await message.channel.send(f"{wks.acell('Y5').value} {wks.acell('Z5').value}")
        await message.channel.send(f"{wks.acell('Y6').value} {wks.acell('Z6').value}")

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

  flatBotChannel = client.get_channel(981536894867345418)
  
  await flatBotChannel.send(f"Hiiiii! This week it is <@{flatmates_ids[num % 3]}>'s turn to take out the kitchen bins and vacuum/broom the hall")

  await flatBotChannel.send(f"<@{flatmates_ids[(num+1) % 3]}>'s turn to clean the toilet and shower - wipe down surfaces, clean the floor, clean the shower :)) ")

  await flatBotChannel.send(f"<@{flatmates_ids[(num+2) % 3]}>'s turn to clean the kitchen. This includes cleaning the surfaces, sweep the floor and use floor wipes for any spillss etc. clean the hob, the microwave (inside too), the fridge (inside as well).")

  update_num()

@aiocron.crontab('0 0 * * mon')
async def cornjob1():
    await printSchedule()


# async def printPaymentDue():
  # read from google sheets and print at the first of every month
  

# @aiocron.crontab('0 0 * * mon,wed,fri,sun')
# @aiocron.crontab('0 0 * * mon')
# async def cornjob1():
#     await printSchedule()

client.run(TOKEN)