import chat_library
import chatIO
import thread

class FakeLibrary(chat_library.ChatLibrary):
	def _connect_(self, user, password, server):
		print "connecting to user: ", user, "with password: ", password, "on server:", server
		self.user=user
		self.password=password
		self.server=server
		thread.start_new_thread(self.mainloop)
		
	def mainloop(self):
		while True:
			self.read(raw_input("Read: "))
	
	def _write_(self, to, message):
		print "Sending message to:",to
		print "-----------------------------------"
		print message
		print "-----------------------------------"
	
	def _disconnect_(self):
		print "disconnecting from server"