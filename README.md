An I/O library for long running applications that will allow them to communicate progress updates to their users over IM protocols like Jabber.


##Usage
The basic design of a program using chatIO can be seen in [usage_example.py](https://github.com/Sheyne/chatIO/blob/master/usage_example.py)	
		

##Python API

**package `chatIO`**



> **class** `IO` 

> > this will be the basic means of communication with a user. It will be expected to be subclassed.

> > **def** `__init__(self, connection, initial_message):`


> > > `connection` is the `Connection` object that received the message.

> > > > It's main purpose is so that `write` knows who to send written messages to.

> > > `initial_message` is the message the `Connection` class received when the user first connected.

> > **def** `read(self, message)`:

> > > Override this method in subclasses.

> > > When the connect user sends a message over IM to the program, this method will be called in a new thread. As such basic thread safety should be practiced when using this method. 

> > **def** `write(self, message)`:

> > > This method takes `message` and sends it over the current chat instance to a the currently connected client.



> **class** `Connection`

> > this initilizes logging in and setting chat status:

> > **def** `__init__(self, chat, io)`:

> > > `chat` is a `ChatLibrary` like object, which will wrap socket communications to the chat server.

> > > `io` is a `chatIO.IO` like class that will be instantiated anytime a new user connects.
> > > When the first message is received from a given user, `io` called with the initial message as a parameter.

> > > > `io` needs to respond to `io(connection = ` `The connection instance` `, initial_message = "` `The initial message` `")` and `io.read(message = "` `The message` `")`.