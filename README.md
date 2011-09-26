An I/O library for long running applications that will allow them to communicate progress updates to their users over IM protocols like Jabber.


##Usage
The basic design of a program using chatIO can be seen in [usage_example.py](https://github.com/Sheyne/chatIO/blob/master/usage_example.py)	
		

##Python API

**package `chatIO`**

> **class** `IO` 

> > this will be the basic means of communication with a user. It will be expected to be subclassed.

> > **def** `__init__(self, initial_message):`

> > > `initial_message` is the message the `Connection` class received when the user first connected.

> > **def** `write(self, message)`:

> > > This method takes `message` and sends it over the current chat instance to a the currently connected client.

> > **def** `read(self, message)`:

> > > This method will be subclassed to allow an chatIO instance to receive chat messages. It will be invoked in a new thread.

> **class** `Connection`

> > this initilizes logging in and setting chat status:

> > **def** `__init__(self, user, password, server, io)`:

> > > `user`, `password` and `server` mediate connecting to the chat server

> > > `io` is a `IO` subclass that will be instantiated anytime a new user connects.
