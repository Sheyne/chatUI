import chatUI
import sys
import unicodedata
import time
import threading
import Queue
import pickle
import datetime

def main():
	# Standard main function. 
	bot = chatUI.UI(server=("talk.google.com", 5223))
	# Setup a connection to a jabber server. 
	# in addition a dictionary of conversationTypes can also be passed.
	
	filename = "chatui_db.pickle"
	
	try:
		with file(filename, "r") as f:
			database = pickle.load(f)
	except (IOError, EOFError):
		database = {}

	# add a conversation type
	# subclasses of chatUI.conversations are initialized when a users first 
	# messages the bot, and until the conversation's `finish()` method is,
	# called. At which point future messages from the same user will create a 
	# new conversation.
	@bot.conversationType
	class default(chatUI.Conversation):
		def setup(self, title):
			split_title = title.split(" ")
			if split_title[0] == "update":
				self.title = ":".join(split_title[1:])
				self.body = database[self.title]
				self.body["last update"] = datetime.date.today()
			
			elif split_title[0] == "delete":
				self.title = ":".join(split_title[1:])
				del database[self.title]
				self.finish(cleanup=False)
				return

			elif title in database:
				self.put(database[title])
				self.finish(cleanup=False)
				return
			else:
				self.title = title
				tod = datetime.date.today()
				self.body = {
					"content": "",
					"tags": set(),
					"created": tod,
					"last update": tod,
				}
		
		def get(self, message):
			message_split = message.split(" ")
			if message_split[0] == "tag":
				self.body["tags"].add(" ".join(message_split[1:]))
			elif message_split[0:2] == ["delete","tag"]:
				self.body["tags"].remove(" ".join(message_split[1:]))
			elif message_split[0:2] == ["clear","tags"]:
				self.body["tags"] = []
			elif message_split[0] == "erase":
				self.body["content"] = ""
			else:
				self.body["content"] += str(message) + "\n"
		
		def cleanup(self):
			database[self.title]=self.body
			self.put("Stored to database with key: %s" % self.title)
			with file(filename, "w") as f:
				pickle.dump(database, f)
		
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
