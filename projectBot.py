from typing import Final
from telegram.ext import ApplicationBuilder
import asyncio

from nltk import chat

TOKEN:Final='8672612277:AAHGUqKgE9u4EJHe8DnEm0kWDYtZAy-ORFg'
username:Final='removeBackground_ChatBot'



if __name__=='__main__':
    application=ApplicationBuilder().token(TOKEN).build()

    application.run_polling() #make it running all the time