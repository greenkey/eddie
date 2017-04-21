""" Unit tests for eddie.endpoints.TelegramEndpoint
"""

import telegram

from eddie.bot import Bot, command
from eddie.endpoints import TelegramEndpoint


def create_telegram_update(message_text):
    """ Helper function: create an "Update" to simulate a message sent to the
        Telegram bot.
    """
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


def test_telegram_interface(mocker):
    """ Test that the Telegram API is called when using the endpoint.
    """

    mock_updater = mocker.patch('eddie.endpoints.telegram.Updater')

    class MyBot(Bot):
        "Lowering bot"

        def default_response(self, in_message):
            return in_message.lower()

    bot = MyBot()

    endpoint = TelegramEndpoint(
        token='123:ABC'
    )
    bot.add_endpoint(endpoint)
    bot.run()

    mock_updater.assert_called_once_with('123:ABC')
    assert mock_updater().start_polling.called

    bot.stop()


def test_telegram_default_response(mocker):
    """ Test that the Telegram bot correctly reply with the default response.
    """

    mocker.patch('eddie.endpoints.telegram.Updater')
    mock_messagehandler = mocker.patch(
        'eddie.endpoints.telegram.MessageHandler')
    reply_text_m = mocker.patch('telegram.Message.reply_text')

    class MyBot(Bot):
        "Uppering-reversing bot"

        def default_response(self, in_message):
            return in_message[::-1].upper()

    bot = MyBot()
    endpoint = TelegramEndpoint(
        token='123:ABC'
    )
    bot.add_endpoint(endpoint)
    bot.run()

    handlers_added = [args for args,
                      kwargs in mock_messagehandler.call_args_list]
    assert len(handlers_added) > 0
    generic_handler = list(handler for filter_, handler in handlers_added)[-1]

    message = 'this is the message'
    generic_handler(bot, create_telegram_update(message))
    reply_text_m.assert_called_with(
        bot.default_response(message))

    bot.stop()


def test_telegram_command(mocker):
    """ Test that the endpoint class correctly registers the commands callback
        and that the Telegram bot uses them to reply to messages.
    """

    mocker.patch('eddie.endpoints.telegram.Updater')
    mock_commandhandler = mocker.patch(
        'eddie.endpoints.telegram.CommandHandler')
    reply_text_m = mocker.patch('telegram.Message.reply_text')

    class MyBot(Bot):
        "Reversing bot"

        def default_response(self, in_message):
            return in_message[::-1]

        @command
        def start(self):
            "start command"
            return 'start command has been called'

        @command
        def other(self):
            "other command"
            return 'other command has been called'

    bot = MyBot()
    endpoint = TelegramEndpoint(
        token='123:ABC'
    )
    bot.add_endpoint(endpoint)
    bot.run()

    commands_added = [args for args,
                      kwargs in mock_commandhandler.call_args_list]
    commands_added = dict((name, handler) for name, handler in commands_added)

    assert 'start' in commands_added
    assert 'other' in commands_added

    commands_added['start'](bot, create_telegram_update('/start'))
    reply_text_m.assert_called_with(bot.start())

    commands_added['other'](bot, create_telegram_update('/other'))
    reply_text_m.assert_called_with(bot.other())

    bot.stop()
