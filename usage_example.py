import chatIO

class MainIO(chatIO.IO):
    def __init__(self, initial_message):
        #configure based on initial message.
        #if no configuration it is common to just call:
        self.read(initial_message)

    def read(self, message):
        #do stuff with message
        self.write("Response") # inform user of the success of the operation


if __name__ == "__main__":
	#note the lack of parens after MainIO
    connection = chatIO.Connection("username", "password", "server", MainIO) 
    
    """Each time a user chats the user that connection logged in as, a new MainIO will be instantiated. Subsequent messages from the same user will call the existing MainIO instance for the user's read methon."""