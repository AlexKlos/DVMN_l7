import os

from dotenv import load_dotenv
from pytimeparse import parse

import ptbot


def render_progressbar(total, iteration, prefix='', suffix='', 
                       length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(time_left, bot, user_id, message_id, sended_time):
    if time_left < sended_time:
        bot.update_message(user_id, message_id, 
                           render_progressbar(sended_time, 
                                              sended_time-time_left, 
                                              'Осталось {} секунд'.format(time_left)))
    if time_left == 0:
        bot.send_message(user_id, 'Время вышло')


def reply(bot, user_id, message):
    sended_time = int(parse(message))
    message_id = bot.send_message(user_id, 
                                  render_progressbar(sended_time, 
                                                     0, 
                                                     'Осталось {} секунд'.format(sended_time)))
    bot.create_countdown(sended_time, notify_progress, bot=bot, user_id=user_id, 
                         message_id=message_id, sended_time=sended_time)
    

def main():
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(lambda user_id, message: reply(bot, user_id, message))
    bot.run_bot()


if __name__ == '__main__':
    main()