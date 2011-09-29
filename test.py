import os
import time

import chatIO


class SampleBot(chatIO.IO):
	pass


if __name__ == "__main__":
	bot = SampleBot()
	@bot.command
	def say(message):
		print "saying message:",message
		os.popen("say "+repr(message))
	@bot.command
	def default(message):
		print "hit default:",message
	
	bot.setState('available', "Active for duty")
	bot.start("comprehend@sheyne.com", "blah1112")