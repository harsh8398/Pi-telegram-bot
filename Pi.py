#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from telegram.ext import Updater, CommandHandler
import urbandictionary as ud
import chucknorris as cn
import random
import logging
import auth_token
from const import START_TEXT, HELP_TEXT

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s\
                    - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(START_TEXT)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(HELP_TEXT)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def throw_slang(bot, update, args):
    """Throws random slang from urban dictionary"""
    if len(args) != 0:
        slang_name = str(" ".join(args))
        slang = ud.define(slang_name)[0]
    else:
        random_slangs = ud.random()
        slang = random.choice(random_slangs)
    update.message.reply_text(slang.word + "\n" + slang.definition + "\n")


def throw_joke(bot, update, args):
    """Throws random joke from chuck norris database"""
    if len(args) != 0:
        fname = args[0]
        if len(args) > 1:
            lname = args[1]
        else:
            lname = ""
        joke = cn.random(fname, lname).joke
    else:
        joke = cn.random().joke
    update.message.reply_text(joke)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(auth_token.get_token())

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("slangme", throw_slang, pass_args=True))
    dp.add_handler(CommandHandler("laughat", throw_joke, pass_args=True))

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
