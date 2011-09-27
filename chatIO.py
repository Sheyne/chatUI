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
	
	def __init__(self, chat, io):
		"""`chat` mediates connecting to the chat server"""
		"""io is a chatIO.IO like class that will be instantiated anytime a new user connects. When the first message is received from a given user, io called with the initial message as a parameter."""
		
		"""io needs to respond to io(connection = The connection instance , initial_message = " The initial message ") and io.read(message = " The message ")."""
		
		# tell `chat` what method to call when a message is received.
		chat.read_method=self.got_message
		
		#initialize empty dictionary of connected users:
		self.connected_users={}
		
		#set the io class:
		self.io_class=io
		

	def got_message(self, sender, message):
		try:
			#try to find io_object in connected_users dictionary
			io_object=self.connected_users[username]
			#if an io_object is found, call its read method in a new thread
			thread.start_new_thread(io_object.read, message)
		except KeyError:
			self.connected_users[username] = self.io_class(connection = self, initial_message = message)

	def __del__(self):
		self.disconnect()
		
	def disconnect(self):
		"""Deals with cleaning up the connection."""
		##disconnect from chat server
	