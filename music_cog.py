from discord.ext import commands 
from discord.utils import get
import discord
import spotify
import YTDL
import asyncio
import random
class Music(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.queue = []
	
	
	@commands.command(help = "Plays a song with the given url or title in the voice chat you'r in", description = "Use with $play <url>")
	async def play(self, ctx, *args):
		url = [" ".join(args).strip()]

		if "spotify" in url[0]:
			url = spotify.spotify(url)
	
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice == None:
			vc = ctx.author.voice
			await vc.channel.connect(cls=discord.VoiceClient)
		
		self.queue += url
		
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice.is_playing():
			pass
		else:
			await self.play_song(voice, ctx)
				
		
		
	@commands.command(help = "Used to pause the player of music", description = "Use $pause")
	async def pause(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice.is_playing():
			voice.pause()
		else:
			await ctx.send("I am not playing music, dumb bitch " + ctx.author.mention)

	@commands.command(help = "Used to join the voice channel youre in", description = "Use $join")
	async def join(self, ctx):
		vc = ctx.author.voice
		if vc == None:
			await ctx.send("You are not connected to a voice channel " + ctx.author.mention)
		else:
			await vc.channel.connect(cls=discord.VoiceClient)
			await ctx.send("I am ready " + ctx.author.mention)
	
	@commands.command(help = "Used to stop the reproduction of music", description = "Use $stop")
	async def stop(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice.is_playing():
			self.queue = []
			voice.stop()
		else:
			await ctx.send("I am not playing music, dumb bitch " + ctx.author.mention)
	
	@commands.command(help = "Used to skip to the next music in queue", description = "Use $next")
	async def next(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice.is_playing():
			voice.stop()
		else:
			await ctx.send("I am not playing music, dumb bitch " + ctx.author.mention)

	@commands.command(help = "Used to resume the player if music is paused", description = "Use $resume")
	async def resume(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice.is_paused():
			voice.resume()
		else:
			await ctx.channel.send("I am rockinggggg " + ctx.author.mention)

	@commands.command(help = "Used to leave the voice channel the bot is in", description = "Use $leave")	
	async def leave(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if(voice == None):
			await ctx.send("I am not connect to a voice Channel " + ctx.author.mention)
		else:
			await voice.disconnect()

	@commands.command(help = "Used to shuffle the queue", description = "Use $shuffle")	
	async def shuffle(self, ctx):
		random.shuffle(self.queue)
		await ctx.send("Shuffle is now on")
	

	async def play_song(self, voice, ctx):
		if len(self.queue) > 0:
			player = await YTDL.YTDLSource.from_url(self.queue[0],stream=True)
			if player != None:
				message = await ctx.send(ctx.author.mention + ' I am now playing: **{}**'.format(player.title))
				voice.play(player, after= lambda e: self.my_after(voice, ctx, message))
				del(self.queue[0])
			else:
				await ctx.send(ctx.author.mention + ' Couldn´t play: **{}**'.format(self.queue[0]))
				del(self.queue[0])
				await self.play_song(voice, ctx)
		else:
			await voice.disconnect()
			await ctx.send(ctx.author.mention + ' I finished the queue')


	def my_after(self, voice, ctx, message):
		coro = self.after_play(voice, ctx, message)

		fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
		try:
			fut.result()
		except:
			pass

	async def after_play(self,voice, ctx, message):
		await message.delete()
		await self.play_song(voice, ctx)

	@commands.command(help = "Shows the queue of songs to be played", description = "Use in form $queue")	
	async def queue(self, ctx):
		l = []
		s = ""
		for i in range(len(self.queue)):
			if i % 10 == 0:
				l.append(s)
				s = ""
			s += str(i+1) + " - " + self.queue[i] + "\n"
		await self.queue_paged(ctx, l[1:])

	async def queue_paged(self, ctx, l):
		cur_page = 1
		message = await ctx.send(f"Page {cur_page}/{len(l)}:\n{l[cur_page-1]}")
		await message.add_reaction("◀️")
		await message.add_reaction("▶️")
		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
		while True:
			try:
				reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
				# waiting for a reaction to be added - times out after x seconds, 60 in this
				# example

				if str(reaction.emoji) == "▶️" and cur_page != len(l):
					cur_page += 1
					await message.edit(content=f"Page {cur_page}/{len(l)}:\n{l[cur_page-1]}")
					await message.remove_reaction(reaction, user)

				elif str(reaction.emoji) == "◀️" and cur_page > 1:
					cur_page -= 1
					await message.edit(content=f"Page {cur_page}/{len(l)}:\n{l[cur_page-1]}")
					await message.remove_reaction(reaction, user)
				else:
					await message.remove_reaction(reaction, user)
			except asyncio.TimeoutError:
				await message.delete()
				break
	@commands.command(help = "Remove element from the queue", description = "Use in form $qdel")
	async def qdel(self, ctx, *args):
		try:
			print(args[0])
			a = int(args[0])
			del[self.queue[a-1]]
		except:
			await ctx.send(ctx.author.mention + ' Wrong command')
		