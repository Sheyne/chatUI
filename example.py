import sys
import pyttsx
import unicodedata
import chatUI
import time
import threading
import Queue



def main():
	# Standard main function. 
	bot = chatUI.UI(server=("talk.google.com", 5223))
	# Setup a connection to a jabber server. 
	# a dictionary of conversationTypes can also be passed.
	
	
	# add a conversation type
	# subclasses of chatUI.conversations are initialized when a users first 
	# messages the bot, and until the conversation's `finish()` method is,
	# called. At which point future messages from the same user will create a 
	# new conversation.
	@bot.conversationType
	class help(chatUI.Conversation):
		usage="conversation_starter [args]"
		def setup(self):
			self.help()
			self.finish()
	
	@bot.conversationType
	class shell(chatUI.ShellConversation):
		description = "shell commands conversation"
		usage = "shell [shutdown, restart]"
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