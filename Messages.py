from cryptography.fernet import Fernet
import os
from discord.ext import commands 
import random


class Dictionary(commands.Cog, name='Automated replys', description = "Use this commands to control everything about your bot system of response to a given word"):
	def __init__(self,bot):
		self.bot = bot
		self.dic = self.read_dic()
		self.prefix = os.getenv("botPrefix")

	@commands.Cog.listener()
	async def on_message(self,message):
		if message.author == self.bot.user:
			return
		if self.check_message(message.content) != False:
			choice = random.choice(self.dic[self.check_message(message.content)])
			await message.channel.send(message.author.mention+" " + choice)
		

	@commands.command(help = "Adds a Automated reply", description = "Use like: $add <message>-<reply>")
	async def add(self,ctx, *args):
		to_add = " ".join(args).strip().split("-", maxsplit=1)
		if len(to_add) < 2:
			await ctx.channel.send(self.error())
			return
		else:
			if (to_add [0] not in self.dic):
				self.dic[to_add[0]] = [to_add[1]]
			elif(to_add[0] in self.dic):
				self.dic[to_add[0]] += [to_add[1]]
		self.save_dic()


	@commands.command(help = "Removes a automated message",description = "Use like: $remove <message>")
	async def remove(self,ctx, *args):
		m = " ".join(args).strip()
		if (m not in self.dic):
			await ctx.send(self.error() +  "and check if the word is in automated replys with **"  + self.prefix + "showCommands**")
			return
		if(m in self.dic):
			del(self.dic[m])
		self.save_dic()

	@commands.command(help = "Shows the automated replys")
	async def showCommands(self,ctx):
		s = "If you send a message with that words in it, bot will reply one of the options:\n"
		s += "**"+self.toString()+"**"
		await ctx.send(s)



	def error(self):
		return "Please check **"  + self.prefix + "help** and send the command in the correct form"

	def check_message(self,message):
		for k in self.dic.keys():
			if k in message.lower():
				return k
		return False

	def toString(self):
		string = ""
		for k,v in self.dic.items():
			string += "\t" + k + " - " 
			for i in range(len(v)-1):
				string += v[i] + "/"
			string += v[len(v)-1]
			string += "\n"
		return string


	def save_dic(self):
		f = Fernet(os.getenv("FernetKey"))
		string = ""
		for k,v in self.dic.items():
			string += k + "«"
			for i in v:
				string += i + "»";
			string += "["
		ciphertext = f.encrypt(string.encode("utf-8"))
		with open("dictionary.obj", "wb") as file:
			file.write(ciphertext)

	def read_dic(self):
		f = Fernet(os.getenv("FernetKey"))
		with open("dictionary.obj", "rb") as file:
			ciphertext = file.read()
		string = f.decrypt(ciphertext)
		decrypted = string.decode('utf8')
		dic = {}
		elements = decrypted.split("[")	
		elements = elements[:len(elements)-1]
		for i in range(len(elements)):
			elements[i] = elements[i].split("«")
			values = elements[i][1].split("»")
			values = values[:len(values)-1]
			dic[elements[i][0]] = values
		return dic