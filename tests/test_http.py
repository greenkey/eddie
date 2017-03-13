from pychatbot.bot import Bot

from http.client import HTTPConnection
import json
from threading import Thread
from urllib.parse import urlencode
from time import sleep


def create_server(b):
	server_thread = Thread(target=b.listen_http)
	server_thread.daemon = True
	server_thread.start()
	
	# wait for server to be up&running
	sleep(0.5)
	
	
def test_http_interface():
	
	class MyBot(Bot):
		def default_response(self, in_message):
			return in_message[::-1]
			
	create_server(MyBot())
		
	test_messages = ["hello", "another message"]
	for tm in test_messages:
		conn = HTTPConnection("127.0.0.1:8000")
		conn.request("GET", "/process?"+urlencode({"in_message":tm}))
		r = conn.getresponse()
		assert r.status == 200
		ret = json.loads(r.read().decode())
		assert ret["out_message"] == tm[::-1]
		conn.close()
