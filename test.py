# v = "0.0.1"

import os
import json
import requests
import time

from copilot import Copilot
from text_to_speech import TextToSpeech
from translate import Translator

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
QUESTION_STATE, 
AUDIO_STATE,) = range(3)


def _generate_copilot(prompt: str):
    """Gets answer from copilot"""
    
    copilot = Copilot()
    c = copilot.get_answer(prompt)

    return c


def _translate(text: str):
    """Translates the text to English"""
    
    translator = Translator()
    t = translator.translate(text)

    return t


def _to_speech(text: str):
    """Converts text to speech"""
    
    tts = TextToSpeech()
    p = tts.to_speech(text)

    return p


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


#Handling the answer
async def pre_query_answer_handler(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    button = [[KeyboardButton(text="Orqaga")], [KeyboardButton(text="Audioni eshitish")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    question = update.message.text

    answer = _generate_copilot(question)
    context.user_data['answer'] = answer

    await update.message.reply_text(
        answer, 
        reply_markup=reply_markup,
    )

    return QUESTION_STATE


#Handling the audio
async def pre_query_audio_handler(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    fp = _to_speech(context.user_data['answer'])

    await update.message.reply_audio(audio=open(fp, 'rb'))

    os.remove(fp)

    return QUESTION_STATE


if __name__ == '__main__':
    load_dotenv()

    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).read_timeout(100).get_updates_read_timeout(100).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ENTRY_STATE: [
                MessageHandler(filters.Regex('^Orqaga$'), start),
                MessageHandler(filters.Regex('^Savol javob$'), pre_query_handler),
            ],
            QUESTION_STATE: [
                MessageHandler(filters.Regex('^Orqaga$'), start),
                MessageHandler(filters.Regex('^Audioni eshitish$'), pre_query_audio_handler),
                MessageHandler(filters.TEXT, pre_query_answer_handler),
            ],
            AUDIO_STATE: [
                MessageHandler(filters.Regex('^Orqaga$'), start),
                MessageHandler(filters.TEXT, pre_query_answer_handler),
            ],
        },
        fallbacks=[],
    )
    
    application.add_handler(conv_handler)

    print("Bot started")
    application.run_polling()
