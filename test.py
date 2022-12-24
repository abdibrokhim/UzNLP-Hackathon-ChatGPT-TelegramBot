import os
import json
import requests
import time

from copilot import Copilot
# from text_to_speech import TextToSpeech
# from text_to_image import TextToImage
# from speech_to_text import SpeechToText
# from translate import Translator

from dotenv import load_dotenv

from telegram import (
    ReplyKeyboardMarkup,
    Update,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    )


(ENTRY_STATE, 
QUESTION_STATE, ) = range(2)

TOKEN = "5975481962:AAENs4gmKt4VA2UGuRDcywmfIVcLjN6K-vA"

def _generate_copilot(prompt: str):
    """Gets answer from copilot"""
    
    copilot = Copilot()
    c = copilot.get_answer(prompt)

    return c


#Starting the bot
async def start(update: Update, context: ContextTypes):
    """Start the conversation and ask user for input."""

    button = [[KeyboardButton(text="Savol javob")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    await update.message.reply_text(
        "Tanlang: 👇🏻",
        reply_markup=reply_markup,
    )

    return ENTRY_STATE
    

#Handling the question
async def pre_query_handler(update: Update, context: ContextTypes):
    """Ask the user for a query."""

    button = [[KeyboardButton(text="Orqaga")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    await update.message.reply_text(
        "Savolingizni yozing: 👇🏻",
        reply_markup=reply_markup,
    )

    return QUESTION_STATE


#Handling the text or audio
# async def ftext_or_audio_handler(update: Update, context: ContextTypes):
#     button = [[KeyboardButton(text="Text ko'rinishida olish"), KeyboardButton(text="Audio ko'rinishida olish")]]
#     reply_markup = ReplyKeyboardMarkup(
#         button, resize_keyboard=True
#     )

#     await update.message.reply_text(
#         "Tanlang: 👇🏻",
#         reply_markup=reply_markup,
#     )

#     return MAIN_STATE


#Handling the answer
async def pre_query_answer_handler(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    question = update.message.text

    answer = _generate_copilot(question)

    await update.message.reply_text(answer)

    return QUESTION_STATE


if __name__ == '__main__':
    load_dotenv()

    application = Application.builder().token(os.getenv(TOKEN)).read_timeout(100).get_updates_read_timeout(100).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ENTRY_STATE: [
                MessageHandler(filters.Regex('^Orqaga$'), start),
                MessageHandler(filters.Regex('^Savol javob$'), pre_query_handler),
            ],
            QUESTION_STATE: [
                MessageHandler(filters.Regex('^Orqaga$'), start),
                MessageHandler(filters.TEXT, pre_query_answer_handler),
            ],
        },
        fallbacks=[],
    )
    
    application.add_handler(conv_handler)

    print("Bot started")
    application.run_polling()
