import time
from telegram import Bot
import hashlib
import requests
import json
import io


from telegram.ext.commandhandler import CommandHandler
from telegram.ext import MessageHandler, MessageFilter, PicklePersistence
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot
import requests 

AUTHENTICATED_KEY = "authenticated"
config = {
    "data_location": 'botdata.dat',
    "auth_token": "AuthTokenValue",
    "bot_token": 'BOT_TOKEN',
}

class AuthenticationFilter(MessageFilter):
    def filter(self, message):
        return config["auth_token"] in message.text

def raise_authenticated(update: Update, context: CallbackContext):
    if not context.user_data.get(AUTHENTICATED_KEY, False):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Unauthenticated")
        raise Exception("Unauthenticated")

def start(update: Update, context: CallbackContext):
    """
    the callback for handling start command
    """
    bot: Bot = context.bot
    auth_key = " ".join(context.args)
    print(auth_key)

    if auth_key != config["auth_token"]:
        bot.send_message(chat_id=update.effective_chat.id, text="Authentication key incorrect!")
        raise Exception("Auth key incorrect")

    context.user_data.clear()
    context.user_data[AUTHENTICATED_KEY] = True
    bot.send_message(chat_id=update.effective_chat.id,
                     text="Initialized, send messages using ckids command. Example: /childmessage Parents of kid 3294 requested")

def childmessage_message(update: Update, context: CallbackContext):
    """
    the callback for handling start command
    """
    raise_authenticated(update, context)

    bot: Bot = context.bot

    try:
        resp = requests.get('http://localhost:62176/html/data/messages')
        json = resp.json()

        message_id = json[0]["id"]
        field_id = json[0]['fields'][0]['id']
        message = " ".join(context.args)

        post_data = {"id":message_id,"fields":[{"id":field_id,"value": message}]}

        requests.post('http://localhost:62176/html/data/request', json=post_data)

        # sending message to the chat from where it has received the message
        # documentation: https://python-telegram-bot.readthedocs.io/en/latest/telegram.bot.html#telegram.Bot.send_message
        bot.send_message(chat_id=update.effective_chat.id,
                        text="Message was sent to beamer team for approval")
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                         text="An error occurred. Please try again later")

while True:
    print("Starting of bot")
    try:
        persistence = PicklePersistence(filename=config["data_location"])
        updater = Updater(config["bot_token"], persistence=persistence, use_context=True)
        dispatcher: Dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler('childmessage', childmessage_message))

        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(e)

    time.sleep(5)

