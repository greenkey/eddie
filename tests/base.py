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
	from urllib.parse import urlencode
	from time import sleep
	
	class MyBot(Bot):
		def default_response(self, in_message):
			return in_message[::-1]
			
	b = MyBot()
	server_thread = Thread(target=b.listen_http)
	server_thread.daemon = True
	server_thread.start()
	
	# wait for server to be up&running
	sleep(0.5)
		
	test_messages = ["hello", "another message"]
	for tm in test_messages:
		conn = HTTPConnection("127.0.0.1:8000")
		conn.request("GET", "/process?"+urlencode({"in_message":tm}))
		r = conn.getresponse()
		assert r.status == 200
		ret = json.loads(r.read().decode())
		assert ret["out_message"] == tm[::-1]
		conn.close()
