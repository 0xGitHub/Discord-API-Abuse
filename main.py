# Discord API abuse to message users that you have blocked, so they have no ability to respond.
# Made By Syntax
# Twitter: @CockSlime
# Github: https://github.com/cannabispowered

# Tested on Python 3.6.8
# With Discord API Version 1.2.5

import discord
import requests
import asyncio
import json

getuser = "https://discord.com/api/v7/users/@me/channels"
dmuser = "https://discord.com/api/v7/channels/"

client = discord.Client()

@client.event
async def on_ready():
	print("Logged in as:", client.user.name+"#"+client.user.discriminator)
	print("UID:", client.user.id)
	print("Discord API Version:", discord.__version__)
	print("Written by Syntax")
	print("Github: https://github.com/cannabispowered")

token = ""

@client.event
async def on_message(message):
	if message.author == client.user:
		commands = []
		z = 0
		for index, a in enumerate(message.content):
			if a == " ":
				commands.append(message.content[z:index])
				z = index + 1

		commands.append(message.content[z:])
		channel = message.channel

		if commands[0] == "#dmuser":
			await message.delete()
			userid = str(commands[1])
			messagecontent = str(commands[2])
			
			headers = {
				"Authorization": token,
				"Content-Type": "application/json"
			}
			r = requests.get('https://discord.com/')
			cookies = {
				'__cfduid' : r.cookies['__cfduid'],
			}

			r = requests.post(getuser, headers=headers, cookies=cookies, data='{"recipient_id":"'+userid'"}')
			data = json.loads(r.text)
			sendmsg = requests.post(dmuser + data['id'] + "/messages", headers=headers, cookies=cookies, data='{"content": "'+messagecontent+'"}')

			if '"code": 50007' in sendmsg.text:
				await channel.send("Error, target user has you blocked.")
			elif 'id' in sendmsg.text:
				await channel.send("Sent!")
			else:
				await channel.send("Unhandled Exception!")
				await channel.send("/shrug")

client.run(token, bot=False)
