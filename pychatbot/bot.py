import json

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
		from http.server import HTTPServer, BaseHTTPRequestHandler
		import http
		from threading import Thread
		from urllib.parse import parse_qs

		PORT = 8000

		class Handler(BaseHTTPRequestHandler):
			def do_GET(s):
				
				function, params = s.path.split("?")
				function, params = function[1:], parse_qs(params)
				
				s.send_response(200)
				s.end_headers()
				output = {
					"out_message": self.process("".join(params["in_message"]))
				}
				s.wfile.write(json.dumps(output).encode("UTF-8"))

		self.httpd = HTTPServer(('', PORT), Handler)
		self.server_thread = Thread(target=self.httpd.serve_forever)
		self.server_thread.daemon = True
		self.httpd.serve_forever()


# decorator    
class command():

	def __init__(self, f):
		Bot.commands.append(f.__name__)
		self.f = f

	def __call__(self):
		return self.f()
