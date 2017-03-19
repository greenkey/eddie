# pychatbot

`pychatbot` is a library you can use to create your own chat bots in seconds.

This is a very young library, any request/suggestion/help will be very
appreciated. For them, create an issue or contact me!

## Install

You can install it downloading this repository in your project or using pip:
```
$ pip install git+ssh://loman@192.168.1.60/~/2TB-BIG/Progetti/personalWorks/pychatbot
```

## Usage

You have to define your bot class, extending the default `Bot` class:
```
>>> from pychatbot.bot import Bot
>>> class MyBot(Bot):
...     pass
... 
>>> b = MyBot()
>>> b
<__main__.MyBot object at 0x7f16e79f3940>

```

Of course you'll want to define some bahaviour, the following chapters teach you how to do it.

### Defining a default response

```
>>> from pychatbot.bot import Bot
>>> class MyBot(Bot):
...     def default_response(self, in_message):
...         # setting echo as default response
...         return in_message
... 
>>> b = MyBot()
>>> b.process("Hello!")
'Hello!'
>>> b.process("Goodbye!")
'Goodbye!'
```

### Defining commands

Just define a method of your Bot class using the `command` decorator.

```
>>> from pychatbot.bot import Bot, command
>>> class MyBot(Bot):
...     @command
...     def hello():
...             return "hello!"
... 
>>> b = MyBot()
>>> b.process("/hello") # the default command prepend is "/"
'hello!'
```

### Defining interfaces

A bot running in local would be pretty useless, isn't it?

The simplest interface we can give to our bot is the http one.

```
>>> from pychatbot.bot import Bot
>>> class MyBot(Bot):
...     def default_response(self, in_message):
...             return in_message
... 
>>> b = MyBot()
>>> b.http_serve()
```

Then you can send message to the bot using simple GET requests (default 
port is 8000): `http://localhost:8000/process?in_message=hello`

The output using the example will be a json with the message: `{"out_message": "hello"}`

### Telegram

Yes, you can easily connect your bot with the Telegram API, thanks to
the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
library.

You don't have to worry about nothing, except getting a token from the
[BotFather](https://core.telegram.org/bots#botfather) and passing it
to your bot.

```
>>> from pychatbot.bot import Bot
>>> class MyBot(Bot):
...     def default_response(self, in_message):
...             return in_message
... 
>>> b = MyBot()
>>> b.telegram_serve(token='123:ABC')
```


## Get involved

If you want to contribute, download the repository, then:

```
$ virtualenv venv # not required but highly suggested
$ source venv/bin/activate
$ pip install -r requirements.txt # install all the requirements
$ pytest
```
