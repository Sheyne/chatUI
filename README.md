An I/O library for long running applications that will allow them to communicate progress updates to their users over IM protocols like Jabber.
#Basics:
Throughout this document a client refers to a person sending Instant Messages, and a server refers to a bot that listens for them. Communications between a client and a server take the form of conversations. A conversation is spawned the first time a specific client sends a message, and all messages from that user will be sent to that conversation until that conversation is over. Once over, new messages will start a new conversation. 

##Usage
The basic design of a program using chatIO can be seen in [usage_example.py](https://github.com/Sheyne/chatUI/blob/master/example.py)

