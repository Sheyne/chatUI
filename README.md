An I/O library for long running applications that will allow them to communicate progress updates to their users over IM protocols like Jabber.

The python API will follow this pattern:

the `chatIO` package will have the following classes:

> `IO` class that will be the basic means of communication with a user. It will be expected to be subclassed.

> > `__init__(self, initial_message):`

> > > `initial_message` is the message the `Connection` class received when the user first connected.

> > `write(self, message)`:

> > > This method takes `message` and sends it over the current chat instance to a the currently connected client.

> > `read(self, message)`:

> > > This method will be subclassed to allow an chatIO instance to receive chat messages. It will be invoked in a new thread.

> `Connection` class, that initilizes logging in and setting chat status:

> > `__init__(self, user, password, server, io)`:

> > > `user`, `password` and `server` mediate connecting to the chat server

> > > `io` is a `IO` subclass that will be instantiated anytime a new user connects.


The basic design of a program using chatIO will be:

	class MainIO(chatIO.IO):
		def __init__(self, initial_message):
			#configure based on initial message.
			#if no configuration it is common to just call:
			self.read(initial_message)
		
		def read(self, message):
			#do stuff with message
			self.write("Response") # inform user of the success of the operation
		
	
	if __name__ == "__main__":
		connection = chatIO.Connection("username", "password", "server", MainIO) #note the lack of parens after MainIO
		#each time a user chats the user that connection logged in as, a new MainIO will be instantiated. 
		#subsequent messages from the same user will call the existing MainIO instance for the user's read methon.