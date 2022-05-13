# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(command_prefix='!', intents=intents)

tracking = None
text = None

@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord!')



@bot.command(name='followme')
async def follow_me(ctx):
	if ctx.author.voice != None:
		global tracking
		tracking = ctx.author
		global text 
		text = ctx.channel
		await ctx.send(f'Now following {tracking.display_name}')
	else:
		await ctx.send(f'Cannot follow {ctx.author.display_name} because they are not in a voice channel')

@bot.command(name='endsession')
async def end_session(ctx):
	global tracking
	if tracking != None:
		await ctx.send(f'Okay, I\'ll leave {tracking.display_name} alone now.')
		for member in tracking.guild.members:
			if member.voice:
				await member.edit(mute=False)
		tracking = None
		global text 
		text = None:
		
	else:
		await ctx.send('I\'m not following anyone right now!')

@bot.event
async def on_voice_state_update(user, before, after):
	global tracking
	channel = tracking.voice.channel
	if tracking != None:
		if tracking.voice == None:
			global text
			for member in tracking.guild.members:
				if member.voice:
					await member.edit(mute=False)
			await text.send(f'Session ended because the user being tracked, {tracking.display_name}, left the channel')
			tracking = None
			text = None
		elif not before.self_mute and after.self_mute and user == tracking:
			print(f'{tracking} has muted themself!')
			for member in channel.members:
				if member.voice.mute != True and member!=tracking:
					await member.edit(mute=True)
					print(f'{member.name} has been server muted!')
		elif before.self_mute and not after.self_mute and user == tracking:
			print(f'{tracking} has unmuted themself!')
			for member in channel.members:
				if member.voice.mute != False:
					await member.edit(mute=False)
					print(f'{member.name} has been server unmuted!')
        
bot.run(TOKEN)