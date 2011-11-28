import xmpp
import inspect
from threading import Thread

class UIError(Exception): pass
class UIUserMessage(UIError): pass
class UIWarning(UIError): pass
class UIUserWarning(UIWarning): pass
class UIUserCommandNotFound(UIUserWarning, UIUserMessage): pass


class Conversation(object):
	description = "Conversation"
	def help(self):
		self.put("Usage: %s" % self.usage)
	def __init__(self, ui, correspondant, initial_message):
		self.ui=ui
		self.initial_message=initial_message
		self.correspondant=correspondant
		self.ui.conversations[self.correspondant]=self
		try:
			self.setup(initial_message)
		except TypeError:
			self.setup() #dont pass args
	
	def setup(self,initial_message=""):
		self.get(self.initial_message)
	
	def shouldFinish(self, message):
		return message == 'done'

	def _get(self, message):
		if self.shouldFinish(message):
			self.finish()
		else:
			self.get(message)
	
	def __str__(self):
		return "%s with %s." % (self.description, self.correspondant)
	
	def cleanup(self): pass
	
	def finish(self,cleanup=True):
		if cleanup:
			self.cleanup()
		try:
			del self.ui.conversations[self.correspondant]
		except KeyError:
			pass
	
	def get(self, message):
		pass
	
	def put(self, message):
		self.ui.send(self.correspondant, message)

class HelpfulConversation(Conversation):
	def __init__(self, ui, correspondant, initial_message):
		super(HelpfulConversation, self).__init__(ui, correspondant, initial_message)
		try:
			if initial_message.split(" ")[1] == 'help':
				self.help()
				self.finish()
		except IndexError:
			pass
		
	def _get(self, message):
		if message=='help':
			self.help()
		elif message in ('describe', 'description'):
			self.help()
		super(HelpfulConversation, self)._get(message)

def command(func):
	func.is_command=True
	return func
	
class ShellConversation(HelpfulConversation):
	def setup(self):
		self.commands = {}
		for name, value in inspect.getmembers(self, inspect.ismethod):
			try:
				if value.is_command:
					self.commands[name] = value
			except AttributeError:
				pass
		self.get(self.initial_message)
		dont_finish=False
		try:
			self.processArgs(self.initial_message.split(" ")[1:])
		except IndexError:
			dont_finish = True
		if not dont_finish:
			self.finish()

	def get(self, message):
		self.processArgs(message.split(" "))
	
	def processArgs(self, args):
		try:
			self.runcommand(args[0],args[1:])
		except KeyError:
			self.runcommand("default",args)
	
	def runcommand(self, command, args):
		try:
			self.commands[command](args)
		except TypeError:
			self.commands[command]()


class UI(object):
	def conversationType(self, cls):
		self.conversationTypes[cls.__name__] = cls
	def command(self, func):
		pass
	def __init__(self, conversationTypes={}, server=("talk.google.com", 5223), debug=[]):
		self.conversationTypes=conversationTypes
		self.debug = debug
		self.server = server
		self.conversations={}

	def start(self, name, password):
		jid=xmpp.JID(name)
		user, server, password = jid.getNode(), jid.getDomain(), password
		
		self.connection=xmpp.Client(server, debug=self.debug)
		connect_success=self.connection.connect( server=self.server )
		if not connect_success:
			raise UIError("Connection to %s failed." % self.server)
			return False
		self.connectionected=True
		if not connect_success in 'tls/ssl':
			raise UIError("SSL/TLS failed.")
		
		auth_success=self.connection.auth(user, password)
		if not auth_success:
			raise UIError("Authentication for %s." % user)
			return False
		if auth_success!="sasl":
			raise UIWarning("sasl not used with %s."%server)
		
		self.connection.RegisterHandler("message", self.received_message)
		self.connection.RegisterHandler('presence',self.received_presence)
		self.connection.sendInitPresence()
		
		if self.connection:
			#available -- dnd -- xa
			pres=xmpp.Presence(priority=5, show="idle", status="Comprehend -- bot")
			self.connection.send(pres)
	
	
	def send(self, to, message):
		self.connection.send(xmpp.Message(to, message))
	
	def mainloop(self):
		while True:
			self.connection.Process()


	def received_presence(self, connection, presence):
		pass
	def received_message(self, connection, message):
		from_user, content = message.getFrom(), message.getBody()
		try:
			Thread(target=self.conversations[from_user]._get, args=(content ,)).start()
		except KeyError:
			command = content.split(" ")[0]
			try:
				conversation_type = self.conversationTypes[command]
			except KeyError:
				try:
					conversation_type = self.conversationTypes["default"]
				except KeyError:
					raise UIUserCommandNotFound("command: '%s' not found" % command, (from_user, content))
			try:
				Thread(target=conversation_type, args=(self, from_user, content)).start()
			except TypeError:
				raise(UIError("Not a conversation-like object"))
