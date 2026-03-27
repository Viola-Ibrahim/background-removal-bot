from typing import Final
import os
from rembg import remove
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# to keep the botToken private
from dotenv import load_dotenv

load_dotenv('token.env')
TOKEN: Final = os.getenv('BOT_TOKEN')
username: Final = 'removeBackground_ChatBot'

os.makedirs("./temp", exist_ok=True)
os.makedirs("./processed", exist_ok=True)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hi, I am a removal bot. to start click on /start")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="To remove a background from an image, please send me the image")


async def process_image(photo_name: str):
    name, _ = os.path.splitext(photo_name)
    output_photo_path = f"./processed/{name}.png"
    input_img = Image.open(f"./temp/{photo_name}")
    output = remove(input_img)
    output.save(output_photo_path)
    os.remove(f'./temp/{photo_name}')
    return output_photo_path


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if filters.PHOTO.check_update(update):
        file_id = update.message.photo[-1].file_id
        unique_file_id = update.message.photo[-1].file_unique_id
        photo_name = f"{unique_file_id}.jpg"

    elif filters.Document.IMAGE:
        file_id = update.message.document.file_id
        _, f_ext = os.path.splitext(update.message.document.file_name)
        unique_file_id = update.message.document.file_unique_id
        photo_name = f"{unique_file_id}{f_ext}"

    photo_file = await context.bot.get_file(file_id)
    await photo_file.download_to_drive(custom_path=f'./temp/{photo_name}')
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='We are processing your photo. Please wait... ')
    processed_image = await process_image(photo_name)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=processed_image)
    os.remove(processed_image)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # commmand handlers
    help_handler = CommandHandler('help', help)
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_message)

    # register commands
    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()  # make it running all the time
