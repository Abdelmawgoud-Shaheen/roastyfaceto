import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os

API_TOKEN = os.getenv("8104310460:AAFuNTe_pp722I40CHvgAmwLrkrzOlx2gqQ")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    web_app_url = "https://roastyfaceto.vercel.app/"  # غيّر هذا بالرابط الحقيقي
    markup.add(InlineKeyboardButton(text="🎮 Start AIBuddy", web_app=WebAppInfo(url=web_app_url)))
    bot.send_message(message.chat.id, "Welcome to AI Buddy!\nTap the button below to start:", reply_markup=markup)

bot.polling()
