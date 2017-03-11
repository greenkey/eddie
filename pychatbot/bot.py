
class Bot():
	commands = []
	command_prepend = "/"
	
	def default_response(self, in_message):
		pass
    
	def process(self, in_message):
		if in_message.startswith(self.command_prepend) and in_message[1:] in self.commands:
			return self.__getattribute__(in_message[1:])()
		return self.default_response(in_message)


# decorator    
class command():

	def __init__(self, f):
		Bot.commands.append(f.__name__)
		self.f = f

	def __call__(self):
		return self.f()
