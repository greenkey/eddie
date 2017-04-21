""" Telegram endpoint for a eddie bot, use this to connect your bot to
    Telegram.

    This module needs `python-telegram-bot` library.
"""

from __future__ import absolute_import
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters


class TelegramEndpoint(object):
    """ Telegram endpoint for a eddie bot, use this to connect your bot to
        Telegram.

        The init needs the token given by the BotFather in order to configure
        with the Telegram service.

        Example usage:

            >>> ep = TelegramEndpoint(
            ...     token='123:ABC'
            ... )
            >>> bot.add_endpoint(ep)
            >>> bot.run()

    """

    def __init__(self, token):
        self._telegram = Updater(token)
        self._token = token
        self._bot = None

    def set_bot(self, bot):
        """ Sets the main bot, the bot must be an instance of
            `eddie.bot.Bot`.

            This method is in charge of registering all the bot's commands and
            default message handlers.

            The commands will be handled by
            `TelegramEndpoint.default_command_handler`, all the other messages
            will be handled by `TelegramEndpoint.default_message_handler`.
        """
        self._bot = bot

        self._telegram.dispatcher.add_handler(
            MessageHandler(
                Filters.text,
                self.default_message_handler
            )
        )

        for command in self._bot.command_names:
            self._telegram.dispatcher.add_handler(
                CommandHandler(
                    command,
                    self.default_command_handler
                )
            )

    def run(self):
        """Starts polling to get the messages."""
        self._telegram.start_polling()

    def stop(self):
        """ Stops polling for new messages.

            Currently this does nothing (TODO)
        """
        pass

    def default_message_handler(self, bot, update):
        """ This is the method that will be called for every new message that
            is not a command. It will ask the bot how to reply to the user.

            The input parameters (`bot` and `update`) are default parameters
            used by telegram.
        """
        in_message = update.message.text
        update.message.reply_text(self._bot.default_response(in_message))

    def default_command_handler(self, bot, update):
        """ All the commands will pass through this method. It will use the
            bot's command to get the output for the user.

            The input parameters (`bot` and `update`) are default parameters
            used by telegram.
        """
        command = update.message.text[1:]
        command_handler = self._bot.__getattribute__(command)
        update.message.reply_text(command_handler())
