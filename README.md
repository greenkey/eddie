# pychatbot

pychatbot is a library you can use to create your own chat bots.

## Install

You can install it downloading this repository in your project or using pip:
```
$ pip install git+ssh://loman@192.168.1.60/~/2TB-BIG/Progetti/personalWorks/pychatbot
```

## Usage

you have to defile your bot class, extending the default `Bot` class:
```
>>> from pychatbot.bot import Bot
>>> class MyBot(Bot):
...     pass
... 
>>> b = MyBot()
>>> b
<__main__.MyBot object at 0x7f16e79f3940>

```

of course you'll want to define some bahaviour, then continue to read.

### Defining a default response

```
>>> from pychatbot.bot import Bot
>>> class MyBot(Bot):
...     def default_response(self, in_message):
...             # setting echo as default response
...             return in_message
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
The simplest interfase we can give to our bot is the http one.

```
>>> from pychatbot.bot import Bot
>>> class MyBot(Bot):
...     def default_response(self, in_message):
...             return in_message
... 
>>> b = MyBot()
>>> b.listen_http()
```

Then you can send message to the bot using simple GET requests (default port il 8000): `http://localhost:8000/process?in_message=hello`
The output uwing the example will be a json with the message: `{"out_message": "hello"}`


## Get involved

If you want to contribute, download the repository, then:

```
$ virtualenv venv # not required but highly suggested
$ source venv/bin/activate
$ pip install -r requirements.txt # install all the requirements
$ pytest
```
