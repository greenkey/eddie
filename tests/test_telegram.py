import telegram

from pychatbot.bot import Bot, command
from pychatbot.endpoints import TelegramEndpoint


def test_telegram_interface(mocker):
    Updater_m = mocker.patch('pychatbot.endpoints.telegram.Updater')

    class MyBot(Bot):
        def default_response(self, in_message):
            return in_message.lower()

    bot = MyBot()

    ep = TelegramEndpoint(
        token='123:ABC'
    )
    bot.add_endpoint(ep)
    bot.run()

    Updater_m.assert_called_once_with('123:ABC')
    assert Updater_m().start_polling.called

    bot.stop()


def create_telegram_update(message_text):
    from datetime import datetime
    message = telegram.Message(
        message_id=0,
        from_user=telegram.User(0, 'greenkey'),
        date=datetime.now(),
        chat=telegram.Chat(0, ''),
        text=message_text
    )

    return telegram.Update(
        update_id=0,
        message=message
    )


def test_telegram_default_response(mocker):
    mocker.patch('pychatbot.endpoints.telegram.Updater')
    MessageHandler_m = mocker.patch(
        'pychatbot.endpoints.telegram.MessageHandler')
    reply_text_m = mocker.patch('telegram.Message.reply_text')

    class MyBot(Bot):

        def default_response(self, in_message):
            return in_message[::-1].upper()

    bot = MyBot()
    ep = TelegramEndpoint(
        token='123:ABC'
    )
    bot.add_endpoint(ep)
    bot.run()

    handlers_added = [args for args,
                      kwargs in MessageHandler_m.call_args_list]
    assert len(handlers_added) > 0
    generic_handler = list(handler for filter_, handler in handlers_added)[-1]

    message = 'this is the message'
    generic_handler(bot, create_telegram_update(message))
    reply_text_m.assert_called_with(
        bot.default_response(message))

    bot.stop()


def test_telegram_command(mocker):
    mocker.patch('pychatbot.endpoints.telegram.Updater')
    CommandHandler_m = mocker.patch(
        'pychatbot.endpoints.telegram.CommandHandler')
    reply_text_m = mocker.patch('telegram.Message.reply_text')

    class MyBot(Bot):

        def default_response(self, in_message):
            return in_message[::-1]

        @command
        def start(self):
            return 'start command has been called'

        @command
        def other(self):
            return 'other command has been called'

    bot = MyBot()
    ep = TelegramEndpoint(
        token='123:ABC'
    )
    bot.add_endpoint(ep)
    bot.run()

    commands_added = [args for args,
                      kwargs in CommandHandler_m.call_args_list]
    commands_added = dict((name, handler) for name, handler in commands_added)

    assert 'start' in commands_added
    assert 'other' in commands_added

    commands_added['start'](bot, create_telegram_update('/start'))
    reply_text_m.assert_called_with(bot.start())

    commands_added['other'](bot, create_telegram_update('/other'))
    reply_text_m.assert_called_with(bot.other())

    bot.stop()
