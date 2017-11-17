#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
"""
from uuid import uuid4

from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent

import urbandictionary as ud
import chucknorris as cn

import os
import random
import logging

from const import START_TEXT, HELP_TEXT, CN_THUMB, UD_THUMB

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s\
                    - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(START_TEXT, parse_mode='HTML')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(HELP_TEXT, parse_mode='HTML')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def _get_slang(args):
    if len(args) != 0:
        slang_name = str(" ".join(args))
        slang = ud.define(slang_name)[0]
    else:
        random_slangs = ud.random()
        slang = random.choice(random_slangs)
    return slang.word + "\n" + slang.definition + "\n"


def _get_joke(args):
    if isinstance(args, str):
        args = args.split(" ")
    if len(args) != 0:
        fname = args[0]
        if len(args) > 1:
            lname = args[1]
        else:
            lname = ""
        joke = cn.random(fname, lname).joke
    else:
        joke = cn.random().joke
    return joke


def throw_slang(bot, update, args):
    """Throws random slang from urban dictionary"""
    slang = _get_slang(args)
    update.message.reply_text(slang, parse_mode='HTML')


def throw_praise(bot, update, args):
    """Throws random joke from chuck norris database"""
    joke = _get_joke(args)
    update.message.reply_text(joke, parse_mode='HTML', quote=False)


def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Slang",
            input_message_content=InputTextMessageContent(
                _get_slang(query),
                parse_mode='HTML'),
            thumb_url=UD_THUMB
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Praise",
            input_message_content=InputTextMessageContent(
                _get_joke(query),
                parse_mode='HTML'),
            thumb_url=CN_THUMB
        )]

    update.inline_query.answer(results)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ['TELEGRAM_TOKEN_BETA'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("slangme", throw_slang, pass_args=True))
    dp.add_handler(CommandHandler("praise", throw_praise, pass_args=True))

    dp.add_handler(InlineQueryHandler(inlinequery))

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
