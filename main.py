import telebot
import uuid
import os
import logging
from PIL import Image

# TOKEN
bot = telebot.TeleBot('')

# Enable logging
logger = telebot.logger

# Outputs debug messages to console
telebot.logger.setLevel(logging.DEBUG)

# Directory with data
global dir_save_data
dir_save_data = ''


# Message handler decorator
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    answer = ''
    if call.data == '1':
        answer = 'В ожидании данных)'
    elif call.data == '2':
        answer = 'Чем больше данных, тем лучше будут обучены модели машинного обучения.'
    bot.send_message(call.message.chat.id, answer)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Прислать фото ' + u'\ud83d\udcf7', callback_data=1))
    markup.add(telebot.types.InlineKeyboardButton(text='Help', callback_data=2))
    bot.send_message(message.chat.id, text="Привет!", reply_markup=markup)


@bot.message_handler(content_types=["document"])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        filename = str(uuid.uuid4())
        path_to_save_file = os.path.join(dir_save_data, filename + '.png')

        with open(path_to_save_file, "wb") as file:
            file.write(downloaded_file)

        image = Image.open(path_to_save_file)

        bot.reply_to(message, "Документ сохранён, спасибо!" + u'\u2714\ufe0f')
    except:
        os.remove(path_to_save_file)
        text_error = 'Прислано не изображение!'
        bot.reply_to(message, text_error)


@bot.message_handler(content_types=["photo"])
def handle_docs_document(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # unique filename
        filename = str(uuid.uuid4())
        path_to_save_file = os.path.join(dir_save_data, filename + '.png')

        with open(path_to_save_file, "wb") as file:
            file.write(downloaded_file)

        bot.reply_to(message, "Фото сохранено, спасибо!" + u'\u2714\ufe0f')
    except Exception as e:
        bot.reply_to(message, e)


if __name__ == '__main__':
    bot.polling()
