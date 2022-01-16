#Files
from alwaysOnline import keep_alive
import Messages
import music_cog
import nacl
import join_play

from discord.ext import commands 
import os


prefix = os.getenv("botPrefix")
client = commands.Bot(command_prefix=prefix)


@client.event
async def on_ready():
	print("Hello, i am GOD BOT")
	
client.add_cog(Messages.Dictionary(client))
client.add_cog(music_cog.Music(client))
client.add_cog(join_play.AutoJoin(client))

keep_alive()
client.run(os.getenv("TOKEN"))