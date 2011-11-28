import chatUI
import sys
import unicodedata
import time
import threading
import Queue



def main():
	# Standard main function. 
	bot = chatUI.UI(server=("talk.google.com", 5223))
	# Setup a connection to a jabber server. 
	# in addition a dictionary of conversationTypes can also be passed.
	
	
	# add a conversation type
	# subclasses of chatUI.conversations are initialized when a users first 
	# messages the bot, and until the conversation's `finish()` method is,
	# called. At which point future messages from the same user will create a 
	# new conversation.
	@bot.conversationType
	class help(chatUI.Conversation):
		description = 'display help'
		usage="conversation_starter [args]"
		def setup(self):
			self.help()
			self.finish()
	
	
	@bot.conversationType
	class commands(chatUI.Conversation):
		description = 'list all posible commands'
		def setup(self, args):
			for command in self.ui.conversationTypes:
				self.put("# %s #\n%s" % (command, self.ui.conversationTypes[command].description))
			self.finish()
	@bot.conversationType
	class pandora(chatUI.ShellConversation):
		description = "pandora commands conversation"
		usage ="""pandora `command'
## Commands
+    love song
-    ban song
a    add music to station
c    create new station
d    delete station
e    explain why this song is played
g    add genre station
h    song history
i    print information about song/station
j    add shared station
m    move song to different station
n    next song
p    pause/continue
q    quit
r    rename station
s    change station
t    tired (ban song for 1 month)
u    upcoming songs
x    select quickmix stations
b    bookmark song/artist
(    decrease volume
)    increase volume
=    delete seeds/feedback"""
		@chatUI.command
		def default(self,command):
			if len(command[0]) == 1:
				with file("/Users/sheyne/.config/pianobar/ctl", "w") as f:
					f.write(command[0])
	@bot.conversationType
	class reply(chatUI.Conversation):
		def setup(self, message):
			self.put(message[6:])
			self.finish()
	@bot.conversationType
	class shell(chatUI.ShellConversation):
		description = "shell commands conversation"
		usage = "shell [shutdown, restart]"
		def restart(self):
			import os
			import sys
			os.system('python example.py')
			sys.exit()
		@chatUI.command
		def time(self):
			self.put(time.strftime('%X %x %Z'))
		@chatUI.command
		def timer(self, args):
			try:
				time.sleep(float(args[0]))
			except ValueError:
				self.put("Bad float")
				return
			self.put(" ".join(args[1:]))
		@chatUI.command
		def default(self):
			pass
	# logon to the server with credentials given.
	bot.start("comprehend@sheyne.com", "blah1112")
	
	while True:
		try:
			bot.mainloop()
		except chatUI.UIUserWarning as message: 
			print message
			bot.send(message[1][0],"%s, type help for help." % message[0])
		except KeyboardInterrupt:
			break


if __name__ == "__main__":
	try:
		main()
	except chatUI.UIError as err:
		print err
