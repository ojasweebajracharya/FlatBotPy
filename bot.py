import json
import discord
from discord.ext import tasks, commands
from datetime import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
import gspread

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
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix = '!', intents=intents)
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

def get_person(person_id):
  print(person_id)
  if person_id == oj_id:
    return "Ojaswee"
  elif person_id == em_id:
    return "Emily"
  elif person_id == sim_id:
    return "Simran"
  else:
    return "Other"

def get_next_free_row_number(starting_letter):
  for i in range(4, 100):
    if wks.acell(f"{starting_letter}{i}").value == None:
      print(i)
      return int(i)
  
  return 0

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    send_message.start()
# COMMANDS ------------------------------------------------

@bot.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# displays balance
@bot.command()
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
@bot.command(aliases=['money-update'])
async def moneyupdate(ctx, *args):

  item = args[0]
  amount = args[1]
  person = args[2]

  row_number = get_next_free_row_number("A")
  if row_number == 0:
    await ctx.send("Errr Emily?? I think the sheet is full :sweat_smile: ")

  if item == None or person == None or amount == None:
    await ctx.send("Your format is incorrect. It should be: money-update {item} {amount} {person}")

  else:
    person = person.lower()

    if get_person(str(ctx.author.id)) == "Other":
      await ctx.send("Who are you? I don't think you're part of this flat...")
      return
    else:
      current_person = get_person(str(ctx.author.id))

    if person == "communal":
      communal_row_number = get_next_free_row_number("N")
      if communal_row_number == 0:
        await ctx.send("Errr Emily?? I think the sheet is full :sweat_smile: ")

      wks.update(f"N{communal_row_number}:P{communal_row_number}", [[item, current_person, float(amount)]])
      await ctx.send("The communal has been updated!")

    else:
      # item and the person who sent the message 
      wks.update(f"A{row_number}:C{row_number}", [[item, current_person, float(amount)]])

      if person == "emily":
        # updates the amount, person and yes/no
        wks.update(f"D{row_number}:E{row_number}", [[float(amount), 'No']])
        await ctx.send(f"I've added Emily owes {current_person} £{amount} for {item}")

      elif person == "simran":
        wks.update(f"F{row_number}:G{row_number}", [[float(amount), 'No']])
        await ctx.send(f"I've added Simran owes {current_person} £{amount} for {item}")

      elif person == "ojaswee":
        wks.update(f"H{row_number}:I{row_number}", [[float(amount), 'No']])
        await ctx.send(f"I've added Ojaswee owes {current_person} £{amount} for {item}")

      else:
        await ctx.send(f"Who is {person}?? Please try again :weary: ")

# clean the money schedule and add cron job to run this once a month

# def runBot():
#   client.on("ready", testChannel())

# cleaning schedule 
# @bot.command(aliases=['cleaning-schedule'])
# async def cleaningschedule(ctx):
#   await printSchedule()

@bot.command(aliases=['cleaning-schedule'])
async def printSchedule(ctx):
  print("TEST 3")
  results = collection.find({"_id":0})
  numArr = [result["num"] for result in results]
  num = numArr[0]

  # flatBotChannel = client.get_channel(981536894867345418)
  flatBotChannel = ctx
  
  await flatBotChannel.send(f"Hiiiii! This week it is <@{flatmates_ids[num % 3]}>'s turn to take out the kitchen bins and vacuum/broom the hall")

  await flatBotChannel.send(f"<@{flatmates_ids[(num+1) % 3]}>'s turn to clean the toilet and shower - wipe down surfaces, clean the floor, clean the shower :)) ")

  await flatBotChannel.send(f"<@{flatmates_ids[(num+2) % 3]}>'s turn to clean the kitchen. This includes cleaning the surfaces, sweep the floor and use floor wipes for any spillss etc. clean the hob, the microwave (inside too), the fridge (inside as well).")
  # update_num()

# async def schedule_daily_message():
#   now = datetime.datetime.now()
#   then = now.datetime.timedelta(days=1)
#   then.replace(hour=19, minute=40)
#   wait_time = (then - now).total_seconds()
#   await asyncio.sleep(wait_time)

#   channel = bot.get_channel(981536894867345418)

#   await channel.send("Good")

@bot.event
async def send_message():
  await bot.wait_until_ready()
  channel = bot.get_channel(981536894867345418)
  channel.send("testing schedule message")

# @tasks.loop(seconds = 15)
# async def checkSunday():
#   print("TEST 3")
#   now = datetime.now()
#   weekday = now.weekday()
#   if weekday == 5:
#     global flatmates_ids  

#     results = collection.find({"_id":0})
#     numArr = [result["num"] for result in results]
#     num = numArr[0]

#     flatBotChannel = client.get_channel(981536894867345418)
    
#     await flatBotChannel.send(f"Hiiiii! This week it is <@{flatmates_ids[num % 3]}>'s turn to take out the kitchen bins and vacuum/broom the hall")

#     await flatBotChannel.send(f"<@{flatmates_ids[(num+1) % 3]}>'s turn to clean the toilet and shower - wipe down surfaces, clean the floor, clean the shower :)) ")

#     await flatBotChannel.send(f"<@{flatmates_ids[(num+2) % 3]}>'s turn to clean the kitchen. This includes cleaning the surfaces, sweep the floor and use floor wipes for any spillss etc. clean the hob, the microwave (inside too), the fridge (inside as well).")
#     update_num()

# CRON FUNCTIONS ------------------------------------------

# @aiocron.crontab('0 0 * * mon')
# async def cornjob1():
#     await printSchedule()

# @aiocron.crontab('0 0 * * mon,wed,fri,sun')
# # @aiocron.crontab('0 0 * * mon')
# @aiocron.crontab('*/5 * * * *')
# async def cornjobSchedule():
#   print("TEST 3")
bot.loop.create_task(send_message())
bot.run(TOKEN)