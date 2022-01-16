from discord.ext import commands 
import discord
from discord.utils import get
import asyncio

class AutoJoin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_voice_state_update(self,member, before, after):
		voice = get(self.bot.voice_clients, guild=member.guild)
		music = "chupaBoiiiiiiii"
		await asyncio.sleep(1)
		if member == self.bot:
			return
		if after.channel == None:
			return
		if member.id == 539456675090923550:
			music = "incrivel"
		elif member.id == 403932087708680240:
			music = "joca"
		elif member.id == 539456675090923550:
			print("Dario")
		elif member.id == 397512857266159638:
			music = "Gtr"
		elif member.id == 638781734078382109:
			music = "FRIDAY"
		elif member.id == 640528490084433930:
			music = "LAB RATS"
		if before.channel != after.channel:
			if voice == None:
				await after.channel.connect(cls=discord.VoiceClient)
				voice = get(self.bot.voice_clients, guild=member.guild)
				voice.play(discord.FFmpegPCMAudio(music + ".mp3"), after = lambda e: self.my_after(voice))
	
	def my_after(self, voice):
		coro = voice.disconnect()
		fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
		try:
			fut.result()
		except:
			pass