import thread

class IO(object):
	"""this will be the basic means of communication with a user. It will be expected to be subclassed."""
	
	def __init__(self, connection, initial_message):	
		"""Connection is the Connection object that received the message.It's main purpose is so that write knows who to send written messages to."""
		
		"""initial_message is the message the Connection class received when the user first connected."""
		
		self.connection = connection
	
	def read(self, message):	
		"""Override this method in subclasses.
		
		When the connect user sends a message over IM to the program, this method will be called in a new thread. As such basic thread safety should be practiced when using this method."""
		
	def write(self, message):		
		"""This method takes message and sends it over the current chat instance to a the currently connected client."""
		
		######## NEED TO ADD ##############################################
		## How the program plans on writing still needs to be ironed out. #
		## It will probably use self.connection                           #
		###################################################################
	
class Connection(object):
	"""this initilizes logging in and setting chat status:"""
	
	def __init__(self, user, password, server, io):
		"""user, password and server mediate connecting to the chat server"""
		
		"""io is a chatIO.IO like class that will be instantiated anytime a new user connects. When the first message is received from a given user, io called with the initial message as a parameter."""
		
		"""io needs to respond to io(connection = The connection instance , initial_message = " The initial message ") and io.read(message = " The message ")."""
		
		##connect to server
		##login with credentials
		
		
		##listen for messages
		
		#initialize empty dictionary of connected users:
		self.connected_users={}
		
		#set the io class:
		self.io_class=io
		
		#start the mainloop:
		thread.start_new_thread(self.mainloop)

	def mainloop(self):
		#when a message is received:
		for username, message in self.receive_messages(): 
			try:
				#try to find io_object in connected_users dictionary
				io_object=self.connected_users[username]
				#if an io_object is found, call its read method in a new thread
				thread.start_new_thread(io_object.read, message)
			except KeyError:
				self.connected_users[username] = self.io_class(connection = self, initial_message = message)
				
	def receive_messages(self):
		self.exit = False
		while not self.exit:
			#the real function would wait for a message to come in
			from time import sleep
			sleep(5)
			yield "Fake_Username", "Fake Message"
		try:
			self.exit()
		except TypeError: #no exit function was specified
			pass
	
	def __del__(self):
		self.exit = self.disconnect
		
	def disconnect(self):
		"""Deals with cleaning up the connection."""
		##disconnect from chat server
	