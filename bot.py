import discord
import os
import aiocron
from dotenv import load_dotenv
# test

load_dotenv()
TOKEN = os.getenv('TOKEN')
client = discord.Client()

flatmates = ["Simran","Ojaswee","Emily","Fraser"]
num = 0

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
    testChannel()
    

def runBot():
  client.on("ready", testChannel())

def printSchedule():
  flatBotChannel = client.channels.cache.get("634765417574957078")
  flatBotChannel.send("Hiiiii! This week it is "+ flatmates[num] + "'s turn to take out the kitchen bins and vacuum the corridor and mop (if needed). ")

  flatBotChannel.send(flatmates[num+1] + "'s turn to clean the bathroom with the shower (clean shower, wipe all surfaces, mop floor? (vacuum? if the floor is dry?))")

  flatBotChannel.send(flatmates[num+2] + "'s turn to clean the smaller bathroom - clean all surfaces, mop floor? vacuum?")

  flatBotChannel.send(flatmates[num+3] + "'s turn to clean the kitchen and sofa areas. This includes vacuuming the floor, mopping, cleaning all surfaces which includes sink, hob, fridge etc.")

  if (num == 3):
    num = 0
    runBot()
  else:
    num += 1
    runBot()

# @aiocron.crontab('0 * * * *')
# async def cornjob1():
#     await flatBotchannel.channel.send('Hour Cron Test')


def testChannel():
  channel = client.get_channel(634765417574957078)
  channel.send('hello')

# client.run(os.environ['TOKEN'])

# this was what was on repl
# import os
# import aiocron
# import discord
# from dotenv import load_dotenv

# load_dotenv()
# TOKEN = os.getenv('TOKEN')

# client = discord.Client()

# @client.event
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')

# flatmates = ["Simran","Ojaswee","Emily","Fraser"]
# num = 0

# def runBot():
#   client.on("ready", printSchedule())

# def printSchedule():
#   flatBotChannel = client.channels.cache.get("895388658885095465")
  
#   flatBotChannel.send("Hiiiii! This week it is "+ flatmates[num] + "'s turn to take out the kitchen bins and vacuum the corridor and mop (if needed). ")

#   flatBotChannel.send(flatmates[num+1] + "'s turn to clean the bathroom with the shower (clean shower, wipe all surfaces, mop floor? (vacuum? if the floor is dry?))")

#   flatBotChannel.send(flatmates[num+2] + "'s turn to clean the smaller bathroom - clean all surfaces, mop floor? vacuum?")

#   flatBotChannel.send(flatmates[num+3] + "'s turn to clean the kitchen and sofa areas. This includes vacuuming the floor, mopping, cleaning all surfaces which includes sink, hob, fridge etc.")

#   if (num == 3):
#     num = 0;
#     runBot()
#   else:
#     num += 1;
#     runBot()

# @aiocron.crontab('0 * * * *')
# async def cornjob1():
#     await flatBotChannel.send('Hour Cron Test')



client.run(TOKEN)

