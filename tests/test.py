from pychatbot.bot import Bot

def test_create_bot_object():
    b = Bot()
    assert isinstance(b, Bot)
    
def test_default_behaviour():
	class MyBot(Bot):
		def default_response(self, in_message):
			return in_message
			
	b = MyBot()
	assert b.process("hello") == "hello"
	assert b.process("123") == "123"
	assert b.process("/hello") == "/hello"
	

def test_add_command():
	from pychatbot.bot import command
	
	class MyBot(Bot):
		@command
		def hello():
			return "hello!"
			
		@command
		def bye():
			return "goodbye..."
		
	b = MyBot()
	assert b.process("/hello") == "hello!"
	assert b.process("/bye") == "goodbye..."
	
def test_http_interface():
	from http.client import HTTPConnection
	import json
	from threading import Thread
	
	class MyBot(Bot):
		def default_response(self, in_message):
			return in_message[::-1]
			
	b = MyBot()
	server_thread = Thread(target=b.listen_http)
	server_thread.daemon = True
	b.listen_http()
	
	conn = HTTPConnection("127.0.0.1:8000")
	conn.request("GET", "/process?in_message=hello")
	r = conn.getresponse()
	assert r.status == 200
	ret = json.loads(r.read().decode())
	assert ret["out_message"] == "olleh"
	conn.close()
	
	conn = HTTPConnection("127.0.0.1:8000")
	conn.request("GET", "/process?in_message=another+message")
	r = conn.getresponse()
	ret = json.loads(r.read().decode())
	assert ret["out_message"] == "egassem rehtona"

