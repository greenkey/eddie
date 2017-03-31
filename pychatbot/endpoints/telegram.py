from __future__ import absolute_import
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters


class TelegramEndpoint(object):

    def __init__(self, token):
        self._telegram = Updater(token)
        self._token = token

    def set_bot(self, bot):
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
        self._telegram.start_polling()

    def stop(self):
        pass

    def default_message_handler(self, bot, update):
        in_message = update.message.text
        update.message.reply_text(self._bot.default_response(in_message))

    def default_command_handler(self, bot, update):
        command = update.message.text[1:]
        f = self._bot.__getattribute__(command)
        update.message.reply_text(f())
