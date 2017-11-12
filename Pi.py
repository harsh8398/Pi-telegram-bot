#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import urbandictionary as ud
import random
import logging
import auth_token

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    keyboard = [[InlineKeyboardButton("/help", callback_data='help')],
                [InlineKeyboardButton("/slangme", callback_data='slangme')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    update.message.reply_text("You can send '/stop' anytime to stop the me.")


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def throw_slang(bot, update):
    """Throws random slang from urban dictionary"""
    random_slangs = ud.random()
    slang = random.choice(random_slangs)
    update.message.reply_text(slang.word + "\n" + slang.definition + "\n")

def inline_keyboard_response(bot, update):
    query = update.callback_query
    {
        'help': help(bot, update),
        'slangme': slangme(bot, update)
    }[query.data]

def reminder(bot, job):
    """Send the alarm message."""
    bot.send_message(job.context, text='Beep!')


def set_reminder(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the reminder in HH:MM,remindtext
        data = args[0].split(",")
        HH = int(data[0].split(":")[0])
        MM = int(data[0].split(":")[1])
        remind_text = str(data[1])

        if HH < 0 or MM < 0:
            update.message.reply_text('If only I had Time Machine!')
            return

        # Add job to queue
        job = job_queue.run_once(reminder, (HH * 60 + MM) * 60, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Reminder successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /remind <HH>:<MM>,<reminder text>')


def rmremind(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('You have no active reminder')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Reminder successfully unset!')


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(auth_token.get_token())

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(inline_keyboard_response))

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("slangme", throw_slang))

    dp.add_handler(CommandHandler("remind", set_reminder,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("rmremind", unset, pass_chat_data=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
