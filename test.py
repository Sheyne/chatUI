import chat_library
import chatIO
import threading
		

class FakeLibrary(chat_library.ChatLibrary):
	def _connect_(self, user, password, server):
		print "connecting to user:", '"'+user+'"', "with password: ", '"'+password+'"', "on server:", '"'+server+'"'
		self.user=user
		self.password=password
		self.server=server
		threading.Thread(target=self.mainloop).start()
		
	def mainloop(self):
		while True:
			self.read(*raw_input("").split(":"))
	
	def _write_(self, to, message):
		print "Sending message to:",to
		print "-----------------------------------"
		print message
		print "-----------------------------------"
	
	def _disconnect_(self):
		print "disconnecting from server"
	
class TestIO(chatIO.IO):
	def init(self):
		print "Inited with message", self.initial_message
	def read(self, message):
		print ">>> ", message
		self.write("got message ")
con=chatIO.Connection(FakeLibrary("sheyne","pass", "talk.google.com"), TestIO)