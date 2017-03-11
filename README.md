# pychatbot

pychatbot is a library you can use to create your own chat bots.

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

## Get involved

If you want to contribute, download the repository, then:

```
$ virtualenv venv # not required but highly suggested
$ source venv/bin/activate
$ pip install -r requirements.txt # install all the requirements
$ pytest
```
