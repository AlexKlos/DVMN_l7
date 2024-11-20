import os

from dotenv import load_dotenv
from pytimeparse import parse

import ptbot


load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

bot = ptbot.Bot(TG_TOKEN)


def render_progressbar(total, iteration, prefix='', suffix='', 
                       length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(time_left, user_id, message_id):
    if time_left < sended_time:
        bot.update_message(user_id, message_id, 
                           render_progressbar(sended_time, 
                                              sended_time-time_left, 
                                              'Осталось {} секунд'.format(time_left)))
    if time_left == 0:
        bot.send_message(user_id, 'Время вышло')


def reply(user_id, message):
    global sended_time
    sended_time = int(parse(message))
    message_id = bot.send_message(user_id, 
                                  render_progressbar(sended_time, 
                                                     0, 
                                                     'Осталось {} секунд'.format(sended_time)))
    bot.create_countdown(sended_time, notify_progress, 
                         user_id=user_id, message_id=message_id)
    

def main():
    bot.reply_on_message(reply)
    bot.run_bot()


if __name__ == '__main__':
    main()