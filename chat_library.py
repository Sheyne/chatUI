import collections

class ChatLibrary(object):
	""" This class will generalize all the chat libraries out there so that chatIO. Can take a chat_library like object and talk to it."""
	connected=False
	def __init__(self, user, password, server, read_method=None):
		"""Initialize with user, pass, server.
		
		Anytime a message is received class `read_method`.
		Parameters for `read_method` are expected to be: (sender, message), where sender is who the message is from and message is the text of the message."""
		self.read_method=read_method
		self.read_queue=[]
		self.connect(user, password, server)
	
	def connect(self, user, password, server):
		"""Connect to `server` with credentials (`user`, `password`)."""
		self.disconnect()
		self._connect_(user, password, server)
		
	def disconnect(self):
		if self.conected:
			self._disconnect_()
	
	def __del__(self):
		self.disconnect()
	
	def write(self, to, message):
		self._write_(to, message)
	
	def read_something(self, sender, message):
		try:
			self.read_message(sender, message)
		except TypeError:
			#self.read_message is not callable, add 
			self.read_queue.append((sender,message))
	
	@property
	def read_method(self):
		return self._read_method
	@read_method.setter
	def read_method(self, read_method):
		self._read_method=read_method
		if isinstance(self._read_method, collections.Callable):
			for sender, message in self.read_queue:
				self.read_something(sender, message)
			self.read_queue=[]
	
	"""Methods to override."""
	#########  Methods to override  ###############
	def _connect_(self, user, password, server):
		"""Override this method in subclasses."""
		###########  Override this ################
		raise(AttributeError, "The function \"_connect_(user, password, server)\" is not defined")
	
	def _write_(self, to, message):
		"""Override this method in subclasses."""
		###########  Override this ################
		raise(AttributeError, "The function \"_write_(to, message)\" is not defined")


	def _disconnect_(self):
		"""Override this method in subclasses."""
		###########  Override this ################
		raise(AttributeError, "The function \"_disconnect_()\" is not defined")
