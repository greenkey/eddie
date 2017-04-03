""" This module contains a set of utility to test pychatbot.

    cfr. http://pytest.org/2.2.4/plugins.html
"""

import pytest


@pytest.fixture
def create_bot():
    """ Fixture - create the bot object given the bot_class and then add the
        endpoint object using the http_class.

        Using the fixture because at the end of the test the webserver is
        closed no matter the test outcome
    """

    fixture = dict()

    def create(bot_class, http_class):
        """ The real function that creates the bot.

            This is needed because the fixture cannot accept parameters.
        """
        fixture['bot'] = bot_class()
        fixture['ep'] = http_class()
        fixture['bot'].add_endpoint(fixture['ep'])
        fixture['bot'].run()

        return fixture['bot']

    yield create

    fixture['bot'].stop()
