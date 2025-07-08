import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os

API_TOKEN = os.getenv("7223539248:AAGGA_BIsoI_USib1fl-H9sOVwHDh8Hovqg")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    web_app_url = "https://mini-ap-ps-85qd.vercel.app/"  # غيّر هذا بالرابط الحقيقي
    markup.add(InlineKeyboardButton(text="🎮 Start AIBuddy", web_app=WebAppInfo(url=web_app_url)))
    bot.send_message(message.chat.id, "Welcome to AI Buddy!\nTap the button below to start:", reply_markup=markup)

bot.polling()
