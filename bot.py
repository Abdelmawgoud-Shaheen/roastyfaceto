import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

API_TOKEN = "ضع_التوكن_الخاص_بالبوت_من_BotFather"

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = WebAppInfo("https://roastyfaceto.vercel.app/")
    btn = KeyboardButton(text="🎨 افتح التطبيق", web_app=web_app)
    markup.add(btn)
    bot.send_message(message.chat.id, "اضغط الزر لفتح تطبيق الذكاء الاصطناعي الخاص بك:", reply_markup=markup)

bot.polling()
