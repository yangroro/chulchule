import re

from slackbot.bot import respond_to, listen_to

@listen_to('^테스트|^pyjog$', re.IGNORECASE)
def test(message):
    message.send('테스트')
