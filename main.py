import discord
from info import get_sentiment
from info import get_PPM
from keep_alive import keep_alive


client = discord.Client()



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
      
  if message.author == client.user:
    return
  
  if message.author.bot == True:
    return

  if message.content == '$sentiment':
    ment = get_sentiment()
    await message.channel.send(ment)

  if message.content.startswith('$ppm'):
    res = get_PPM()
    await message.channel.send(res)
    

keep_alive()
client.run("ODYwOTMyNTk2NzU4MDg1NzAy.YOCb9g.v0OX6JgSfAqtl224bRNIMcokfMo")