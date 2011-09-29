import sys
import os
import unicodedata
import chatUI

class DefaultConversation(chatUI.Conversation):
	def get(self, message):
		print message
	
class ShellConversation(chatUI.Conversation):
	def setup(self, initial_message):
		pass
	def get(self, c):
		if c == 'shutdown':
			sys.exit()
		elif c == 'restart':
			print 'restarting, can\'t'
		else:
			print message
	
class SayConversation(chatUI.Conversation):
	def setup(self, initial_message):
		args_s=self.initial_message.split(" ")[1:]
		self.args=" ".join(args_s)+" "
	def get(self, message):
		process="say "+self.args+repr(unicodedata.normalize('NFKD', message).encode('ascii','ignore'))
		print process
		os.popen(process)


if __name__ == "__main__":
	bot = chatUI.UI()
	
	#bot.conversationTypes["default"]=DefaultConversation
	bot.conversationTypes["say"]=SayConversation
	bot.conversationTypes["shell"]=ShellConversation
	bot.conversationTypes["/"]=ShellConversation
	
	bot.start("comprehend@sheyne.com", "blah1112")
	
	
