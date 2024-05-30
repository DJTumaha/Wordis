import telebot
from telebot import types
import requests
import json


bot = telebot.TeleBot('6684226186:AAHxwwXemVjBHG5JFLdYUbRCLjLiq_LklOE')

words_headers = {"X-RapidAPI-Key": "bfc24b8ebdmshbb8ac8aad2f05a7p1bcb08jsn8d5cf2cea6e1",
                 "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"}


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    bot.send_message(message.chat.id,
                     f'Hi, {message.from_user.first_name}! '
                     'Please write a word to find the meaning of it!\n',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_request(message):
    request = message.text.strip().lower()
    words_response = requests.get(f"https://wordsapiv1.p.rapidapi.com/words/{request}/typeOf", headers=words_headers)
    words_data = json.loads(words_response.text)
    if words_response.status_code == 200:
        bot.reply_to(message, f'{words_data["word"]} means:\n\n1: {words_data["typeOf"][0]}'
                              f'\n2: {words_data["typeOf"][1]}'
                              f'\n3: {words_data["typeOf"][2]}')
    else:
        bot.reply_to(message, f"Unfortunately, we can't find this word. Try another one!")


bot.polling(non_stop=True)
