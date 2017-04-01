from distutils.core import setup


setup(
    name='pychatbot',
    packages=['pychatbot', 'pychatbot.endpoints'],
    version='0.7.0',
    description='A lib to create chatbots',
    author='Lorenzo Mele',
    author_email='greenkey@loman.it',
    keywords=['chatbot', 'telegram'],
    install_requires=['python-telegram-bot'],
)
