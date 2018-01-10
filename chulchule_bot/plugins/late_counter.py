# -*- coding:utf-8 -*-
import re
from datetime import date

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from slackbot import settings
from slackbot.bot import listen_to
from slackbot.dispatcher import Message
from slacker import Slacker


def get_late_count_dict(channel_id: str, messages: list, target_date: date) -> dict:
    slacker = Slacker(settings.API_TOKEN)
    late_info = slacker.groups.info(channel_id).body['group']['members']
    late_info = {key: None for key in late_info}
    for user in late_info:
        user_name = slacker.users.info(user).body['user']['profile']['real_name']
        late_info[user] = {
            'late_dates': [],
            'user_name': user_name
        }
    for message in messages:
        if message.get('user'):
            user = message.get('user')
            for line in message['text'].split('\n'):
                try:
                    late_date = parse(line, fuzzy=True)
                except ValueError:
                    continue
                if late_date.year == target_date.year and late_date.month == target_date.month:
                    late_info[user]['late_dates'].append(late_date)
    return late_info


def make_late_count_message(target_date: date, late_info: dict) -> str:
    message = f"```{target_date.year}년 {target_date.month}월 지각리스트\n"

    for user in late_info:
        late_info[user]['late_dates'] = set(late_info[user]['late_dates'])
        count = len(late_info[user]['late_dates'])
        late_info[user]['count'] = count
        line = f"{late_info[user]['user_name']}: {late_info[user]['count']}\n"
        if count != 0:
            message += line
    message += "```"
    return message


def make_late_count_detail_message(target_date: date, late_info: dict) -> str:
    message = f"```{target_date.year}년 {target_date.month}월 지각 상세 리스트\n"

    for user in late_info:
        late_info[user]['late_dates'] = set(late_info[user]['late_dates'])
        message += f"{late_info[user]['user_name']}: \n"
        for late_date in late_info[user]['late_dates']:
            line = f"    {late_date.strftime('%Y-%m-%d')}\n"
            message += line
    message += "```"
    return message


@listen_to('^지각!', re.IGNORECASE)
def late_count(message_info: Message):
    message = message_info.body['text']
    if message.find('이번달') != -1:
        target_date = date.today()
    else:
        try:
            target_date = parse(message, fuzzy=True).date()
        except ValueError:
            target_date = date.today() - relativedelta(months=1)

    slacker = Slacker(settings.API_TOKEN)
    channel_id = message_info.channel._body['id']
    response = slacker.groups.history(channel_id, count=1000)
    messages = response.body['messages']

    late_info = get_late_count_dict(channel_id, messages, target_date)

    if message.find('상세') != -1:
        message = make_late_count_detail_message(target_date, late_info)
    else:
        message = make_late_count_message(target_date, late_info)

    message_info.send(message)
