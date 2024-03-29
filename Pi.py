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
        slang = ud.define(slang_name, embedd_link=True)[0]
    else:
        random_slangs = ud.random(embedd_link=True)
        slang = random.choice(random_slangs)
    return slang.word + "\n" + slang.definition + "\n"


def _get_joke(args):
    joke = cn.random().joke
    if isinstance(args, list):
        args = ' '.join(args)
    if len(args) != 0:
        joke = joke.replace("Chuck Norris", args)
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

    TOKEN = os.environ['TELEGRAM_TOKEN_DEPLOY']
    NAME = os.environ['HEROKU_APP_NAME']

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

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

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()


if __name__ == '__main__':
    main()
