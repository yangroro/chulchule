# -*- coding:utf-8 -*-
import re
from dateutil.parser import parse

from slackbot import settings
from slackbot.bot import listen_to
from slacker import Slacker


@listen_to('^이번달 지각리스트', re.IGNORECASE)
def late_count(message_info):
    slacker = Slacker(settings.API_TOKEN)
    channel_id = message_info.channel._body['id']
    response = slacker.channels.history(channel_id, count=100)
    messages = response.body['messages']
    users = slacker.channels.info(channel_id).body['channel']['members']
    users = {key: None for key in users}
    for user in users:
        users[user] = []
    for message in messages:
        if message.get('user'):
            user = message.get('user')
            for line in message['text'].split('\n'):
                try:
                    late_date = parse(line, fuzzy=True)
                except ValueError:
                    continue
                users[user].append(late_date)
    print('end')
    print(users)
