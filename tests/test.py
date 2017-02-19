

def test_create_bot_object():
    from pychatbot.bot import Bot
    b = Bot()
    assert isinstance(b, Bot)
