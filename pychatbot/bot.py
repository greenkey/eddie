
class Bot():
	commands = []
	command_prepend = "/"
	
	def default_response(self, in_message):
		pass
    
	def process(self, in_message):
		if in_message.startswith(self.command_prepend) and in_message[1:] in self.commands:
			return self.__getattribute__(in_message[1:])()
		return self.default_response(in_message)
		
	def listen_http(self):
		from http.server import HTTPServer
		import http

		PORT = 8000

		class Handler(http.server.BaseHTTPRequestHandler):
			def do_GET(s):
				s.send_response(200)
				s.send_header("Content-type", "text/html")
				s.end_headers()
				s.wfile.write(b'{"out_message": "olleh"}')

		server_class = HTTPServer
		self.httpd = server_class(('', PORT), Handler)
		self.httpd.serve_forever()
		



# decorator    
class command():

	def __init__(self, f):
		Bot.commands.append(f.__name__)
		self.f = f

	def __call__(self):
		return self.f()
