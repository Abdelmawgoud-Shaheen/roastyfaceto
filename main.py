import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import requests
import cv2
import numpy as np

API_TOKEN = "8104310460:AAFuNTe_pp722I40CHvgAmwLrkrzOlx2gqQ"

bot = telebot.TeleBot(API_TOKEN)

# ---------- Helper: Check if image has a human face ----------
def has_face(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces) > 0

# ---------- Helper: Call HuggingFace AI API (Secure) ----------
def analyze_image_with_ai(image_bytes):
    HUGGINGFACE_API_KEY = os.getenv("HF_TOKEN")  # Secure environment variable

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }

    files = {
        'inputs': ('image.jpg', image_bytes, 'image/jpeg')
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base",
        headers=headers,
        files=files
    )

    if response.status_code == 200:
        result = response.json()
        caption = result[0]["generated_text"]
        return f"🔥 Roast caption: {caption}"
    else:
        return "⚠️ Failed to analyze the image. Please try again later."

# ---------- Handle /start command ----------
@bot.message_handler(commands=["start"])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = WebAppInfo("https://roastyfaceto.vercel.app/")
    btn = KeyboardButton(text="🎨 Open the App", web_app=web_app)
    markup.add(btn)
    bot.send_message(message.chat.id, "Click the button below to open the AI roast app:", reply_markup=markup)

# ---------- Handle shared data from WebApp ----------
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    data = message.web_app_data.data
    bot.send_message(message.chat.id, f"✅ Data received from web app: {data}")

# ---------- Handle photo uploads ----------
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    image = bot.download_file(file_info.file_path)

    if not has_face(image):
        bot.reply_to(message, "😅 No clear human face detected. Please send a photo with a visible person.")
        return

    roast = analyze_image_with_ai(image)
    bot.reply_to(message, roast)

bot.polling()
