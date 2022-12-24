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
    filters,)

TOKEN = "5975481962:AAEJqH17EpW0OgFqcSvoWibG3KnkF_7JGP4"



(
ENTRY_STATE,

QA_STATE,
IMAGE_STATE,

QA_START_WITH_TEXT, #Sending text
QA_START_WITH_AUDIO, #Sending audio
#
IG_START_WITH_TEXT, #Sending text
IG_START_WITH_AUDIO, #Sending audio
#
OUTPUT_TEXT,
OUTPUT_AUDIO,
#
QA_INPUT_TEXT,
QA_INPUT_AUDIO,
#
IG_INPUT_TEXT,
IG_INPUT_AUDIO,
#
QA_TEXT_AUDIO,
QA_TEXT_TEXT,
#
QA_MALE,
QA_FEMALE,
#
QA_TEXT_HANDLER,
QA_AUDIO_HANDLER,
IG_TEXT_HANDLER,
IG_AUDIO_HANDLER,
#
END
) = range(22)


#Starting the bot
async def start(update: Update, context: ContextTypes):
    """Start the conversation and ask user for input."""

    button = [[KeyboardButton(text="Question-Answering"), KeyboardButton(text="Image Generator")]]
    # reply_keyboard = ["Book", "Audio"]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text(
        "Choose an option below:👇🏻",
        reply_markup=reply_markup,
    )

    return ENTRY_STATE

# First step
async def quest_answer(update: Update, context: ContextTypes): #Question answering menu
    """Enters to QA menu and gives 2 buttons"""

    button = [
        [KeyboardButton(text="QA TEXT"), KeyboardButton(text="QA AUDIO")],
        [KeyboardButton(text="Back 🔙")],
    ]

    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

    return QA_STATE


async def image_gen(update: Update, context: ContextTypes): #Image generator menu
    """Enters to IG menu and gives 2 buttons"""

    button = [
        [KeyboardButton(text="IG TEXT"), KeyboardButton(text="IG AUDIO")],
        [KeyboardButton(text="Back 🔙")],
    ]

    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

    return IMAGE_STATE

#Second Step -----> QA - Menu 

async def qa_with_text(update: Update, context: ContextTypes): #QA Menu ----> To ask input as text
    """Enters to QA TEXT menu and gives 2 buttons"""

    button = [
        [KeyboardButton(text="Textda olish"), KeyboardButton(text="Audioda olish")],
        [KeyboardButton(text="Back 🔙")],
    ]

    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)


    return QA_START_WITH_TEXT

async def qa_with_audio(update: Update, context: ContextTypes):  #QA Menu ----> To ask input as audio
    """Enters to QA AUDIO menu and gives 2 buttons"""

    button = [
        [KeyboardButton(text="Textda olish"), KeyboardButton(text="Audioda olish")],
        [KeyboardButton(text="Back 🔙")],
    ]

    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True, one_time_keyboard=True
    )
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

    return QA_START_WITH_AUDIO


#Second Step -----> IG - Menu 

async def ig_with_text(update: Update, context: ContextTypes): #QA Menu ----> To ask input as text
    """Enters to QA TEXT menu and aks text"""

    await update.message.reply_text("Describe picture in text in Uzbek:")

    return IG_START_WITH_TEXT

async def ig_with_audio(update: Update, context: ContextTypes):  #QA Menu ----> To ask input as audio
    """Enters to QA AUDIO menu and asks an audio"""

    await update.message.reply_text("Describe a picture in audio in Uzbek:")

    return IG_START_WITH_AUDIO



#Third step ---> QA Menu
async def qa_text_reciever(update: Update, context: ContextTypes):
    """Enters to QA WITH TEXT menu and asks input as text"""

    await update.message.reply_text("Type text in Uzbek ")


    return QA_INPUT_TEXT

async def qa_audio_reciever(update: Update, context: ContextTypes): 
    """Enters to QA WITH TEXT menu and asks input as audio"""


    
    await update.message.reply_text("Send an audio in Uzbek")

    return QA_INPUT_AUDIO

# #Third step ---> IG Menu
# async def ig_text_reciever(update: Update, context: ContextTypes):
#     """Enters to QA WITH TEXT menu and asks input as text"""

#     await update.message.reply_text("Describe image on text:")

#     return IG_INPUT_TEXT

# async def ig_audio_reciever(update: Update, context: ContextTypes): 
#     """Enters to QA WITH TEXT menu and asks input as text"""

#     await update.message.reply_text("Describe an image on audio in Uzbek:")

#     return IG_INPUT_AUDIO

#Fourth step ---> QA Menu
async def qa_text_handler(update: Update, context: ContextTypes):
    """Holds input text"""

    text = update.message.text.lower()
    context.user_data["choice"] = text

    return QA_TEXT_HANDLER

async def qa_audio_handler(update: Update, context: ContextTypes): 
    """Holds sended audio"""
    audio = update.message.audio
    context.user_data["choice"] = audio

    return QA_AUDIO_HANDLER

#Fourth step ---> IG Menu
async def ig_text_handler(update: Update, context: ContextTypes):
    """Holds input text"""

    text = update.message.text.lower()
    context.user_data["choice"] = text

    return IG_TEXT_HANDLER

async def ig_audio_handler(update: Update, context: ContextTypes): 
    """Holds sended audio"""
    audio = update.message.audio
    context.user_data["choice"] = audio

    print(audio)

    return IG_AUDIO_HANDLER


def main():
    """Run the bot"""
    application = Application.builder().token(TOKEN).read_timeout(100).get_updates_read_timeout(100).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ENTRY_STATE: [
                MessageHandler(filters.Regex("^Question-Answering$"),quest_answer),
                MessageHandler(filters.Regex("^Image Generator$"),image_gen),
            ],


            QA_STATE: [
                MessageHandler(filters.Regex("^QA TEXT$"), qa_with_text),
                MessageHandler(filters.Regex("^QA AUDIO$"), qa_with_audio),
                MessageHandler(filters.Regex("^Back 🔙$"), start),
            ],
            IMAGE_STATE: [
                MessageHandler(filters.Regex("^IG TEXT$"), ig_with_text),
                MessageHandler(
                    filters.Regex("^IG AUDIO$"), ig_with_audio
                ),
                MessageHandler(filters.Regex("^Back 🔙$"), start),
            ],


           QA_START_WITH_TEXT: [
                MessageHandler(filters.Regex("^Textda olish$"), qa_text_reciever),
                MessageHandler(filters.Regex("^Audioda olish$"), qa_audio_reciever),
                MessageHandler(filters.Regex("^Back 🔙$"), quest_answer),
            ],
            QA_START_WITH_AUDIO: [
                MessageHandler(filters.Regex("^Textda olish$"), qa_text_reciever),
                MessageHandler(filters.Regex("^Audioda olish$"), qa_audio_reciever),
                MessageHandler(filters.Regex("^Back 🔙$"), quest_answer),
            ],
            IG_START_WITH_TEXT: [
                MessageHandler(filters.TEXT, ig_with_text),
                MessageHandler(filters.Regex("^Back 🔙$"), image_gen),
            ],
            IG_START_WITH_AUDIO: [
                MessageHandler(filters.AUDIO, ig_with_audio),
                MessageHandler(filters.Regex("^Back 🔙$"), image_gen),
            ],

            QA_INPUT_TEXT: [
                MessageHandler(
                    filters.TEXT,
                    qa_text_handler,
                ),
                MessageHandler(filters.Regex("^Back 🔙$"), start),
            ],
            QA_INPUT_AUDIO: [
                MessageHandler(
                    filters.AUDIO,
                    qa_audio_handler,
                ),
                MessageHandler(filters.Regex("^Back 🔙$"), start),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        map_to_parent={END: ENTRY_STATE},
    )



    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()