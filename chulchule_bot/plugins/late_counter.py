# -*- coding:utf-8 -*-
import re

from slackbot import settings
from slackbot.bot import listen_to
from slacker import Slacker


@listen_to('^이번달 지각리스트', re.IGNORECASE)
def late_count(message_info:
    slacker = Slacker(settings.API_TOKEN)

    channel_id = message_info.channel._body['id']
    history = slacker.channels.history(channel_id, count=1000)

    users = []
    for message in history:


