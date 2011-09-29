import xmpp


class UIError(Exception):
	pass
class UIWarning(UIError):
	pass
class UIUserWarningMessage(UIWarning):
	pass
class UICommandNotFoundWarningMessage(UIUserWarningMessage):
	pass

class Conversation(object):
	def __init__(self, ui, correspondant, initial_message):
		self.ui=ui
		self.initial_message=initial_message
		self.correspondant=correspondant
		self.setup(initial_message)
	
	def setup(self,initial_message=""):
		self.get(self.initial_message)
	
	def shouldFinish(self, message):
		return message == 'done'

	def _get(self, message):
		if self.shouldFinish(message):
			self.finish()
		else:
			self.get(message)
			
	def finish(self):
		del self.ui.conversations[self.correspondant]
	
	def get(self, message):
		pass
	
	def put(self, message):
		self.ui.send(self.correspondant, message)
	
	def end(self):
		self.ui.removeConversation(self)

class UI(object):
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
			raise UIError("Authentication for %s.", user)
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

		self.mainloop()
	
	
	def send(self, to, message):
		self.connection.send(xmpp.Message(to, message))
	
	def mainloop(self):
		while True:
			try:
				self.connection.Process()
			except UIUserWarningMessage as e:
				self.send(e.args[1][0], "Unknown command: %s" % str(e.args[1][1]))
			except KeyboardInterrupt: 
				break


	def received_presence(self, connection, presence):
		pass
	def received_message(self, connection, message):
		from_user, content = message.getFrom(), message.getBody()
		try:
			self.conversations[from_user]._get(content)
		except KeyError:
			command = content.split(" ")[0]
			try:
				conversation_type = self.conversationTypes[command]
			except KeyError:
				try:
					conversation_type = self.conversationTypes["default"]
				except KeyError:
					raise UICommandNotFoundWarningMessage("command: '%s' not found" % command, (from_user, content))
			try:
				self.conversations[from_user]=conversation_type(self, from_user, content)
			except TypeError:
				raise(UIError("Not a conversation-like object"))
