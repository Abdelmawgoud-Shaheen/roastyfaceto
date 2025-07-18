import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

API_TOKEN = os.getenv("8104310460:AAFuNTe_pp722I40CHvgAmwLrkrzOlx2gqQ")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = WebAppInfo("https://roastyfaceto.vercel.app/")
    btn = KeyboardButton(text="🎨 افتح التطبيق", web_app=web_app)
    markup.add(btn)
    bot.send_message(message.chat.id, "اضغط الزر لفتح التطبيق:", reply_markup=markup)

bot.polling()
