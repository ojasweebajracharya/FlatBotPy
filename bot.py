from ast import alias
import json
import discord
from discord.ext import commands
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

# needed for it to work, Why?? Should probably check at some point?
intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('TOKEN')
client = commands.Bot(command_prefix = '!', intents=intents)
# client = discord.Client(intents=intents)
oj_id = "571276422363217951"
em_id = "238389040187965441"
sim_id = "719261320662351950"
flatmates_ids = [em_id, sim_id, oj_id]

sa = gspread.service_account(filename = 'service_account.json')
sh = sa.open("Money")
wks = sh.worksheet("Monthly")
spreadsheet_id = "1iPj_UJp5D-LJJFSppaZTyJEqQvPjMi2YUPMN7c3-tbg"
sheet_id = 0

# updates the mongo db database, increases number for the rota 
def update_num():
  collection.update_one({"_id":0},{ "$inc": {"num": +1}})

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# COMMANDS ------------------------------------------------

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# displays balance
@client.command()
async def money(ctx, *, person = None):

  em_message = f"""**{wks.acell('Y4:Z4').value}** \n{wks.acell('Y5').value} {wks.acell('Z5').value} \n{wks.acell('Y6').value} {wks.acell('Z6').value} \n"""
  sim_message = f"""**{wks.acell('Y8:Z8').value}** \n{wks.acell('Y9').value} {wks.acell('Z9').value} \n{wks.acell('Y10').value} {wks.acell('Z10').value} \n"""
  oj_message = f"""**{wks.acell('Y12:Z12').value}** \n{wks.acell('Y13').value} {wks.acell('Z13').value} \n{wks.acell('Y14').value} {wks.acell('Z14').value} \n"""

  if person == None: 
    await ctx.send(em_message)
    await ctx.send(oj_message)
    await ctx.send(sim_message)
  
  else:
    person = person.lower()

    if person == "emily":
      await ctx.send(em_message)
    
    elif person == "simran":
      await ctx.send(sim_message)

    elif person == "ojaswee":
      await ctx.send(oj_message)
    
    else:
      await ctx.send("Who is that?? Please try again :weary: ")

# updates people and communal (person = communal if it was communal)
@client.command(aliases=['money-update'])
async def moneyupdate(ctx, *args):
  # arguments = ', '.join(args)
  # await ctx.send(f'{len(args)} arguments: {arguments}')

  item = args[0]
  amount = args[1]
  person = args[2]

  await ctx.send(f"{item}, {amount}, {person}")

  if item == None:
    await ctx.send("You didn't include an item :(")

  if amount == None:
    await ctx.send("How much does it cost?")

  if person == None:
    await ctx.send("You didn't include a person :( Please try again :smile: ")
  
  else:
    person = person.lower()

    if person == "emily":
      # so item and then the person who sent the message 
      wks.update("A4:C4", [item, 'Ojaswee', amount])
      # then this bit updates the amount, person and yes/no
      wks.update("D4:E4", [amount, 'No'])

      await ctx.send(f"I've added Emily owes Ojaswee £{amount} for {item}")

    elif person == "simran":
      pass
    elif person == "ojaswee":
      pass
    elif person == "communal":
      pass
    else:
      await ctx.send(f"Who is {person}?? Please try again :weary: ")


    
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
@aiocron.crontab('0 0 * * mon')
async def cornjob1():
    await printSchedule()

client.run(TOKEN)