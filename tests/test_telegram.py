import telegram

from pychatbot.bot import Bot, command


def test_telegram_interface(mocker):
	
	class MyBot(Bot):
		def default_response(self, in_message):
			return in_message.lower()
			
	bot = MyBot()
	
	mocker.patch('telegram.ext.Updater')

	bot.telegram_serve(
		token='123:ABC'
	)
	
	telegram.ext.Updater.assert_called_once_with('123:ABC')
	assert telegram.ext.Updater().start_polling.called




