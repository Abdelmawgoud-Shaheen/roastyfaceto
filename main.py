from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import telebot
import traceback
import os

# ✅ قراءة متغيرات البيئة
API_TOKEN = os.environ.get("BOT_TOKEN")
BASE_URL = os.environ.get("BASE_URL")  # مثال: https://your-app.up.railway.app

# ✅ تحقق من وجود التوكن
if not API_TOKEN:
    raise ValueError("❌ BOT_TOKEN is missing. Please set it in Railway environment variables.")

# ✅ إعداد البوت
bot = telebot.TeleBot(API_TOKEN)

# ✅ إعداد Flask
app = Flask(__name__)
CORS(app)

# ✅ الصفحة الرئيسية
@app.route("/")
def index():
    return "✅ RoastyFaceTo AI backend is running."

# ✅ نقطة استقبال الصور من الواجهة (Vercel)
@app.route("/roast", methods=["POST"])
def roast_image():
    print("🚀 Received POST /roast request")

    if "image" not in request.files:
        print("❌ No image found in request.files")
        return jsonify({"result": "❌ No image received."}), 400

    image_file = request.files["image"]
    print(f"📁 Received file: {image_file.filename}")

    try:
        image = Image.open(image_file.stream)
        print("✅ Image opened successfully")

        # 🧠 هذا مكان إدراج الذكاء الاصطناعي لاحقًا
        roast_text = "🔥 That face could scare a mirror! 😂"

        print("✅ Roast generated:", roast_text)
        return jsonify({"result": roast_text})

    except Exception as e:
        print("❌ Error during image processing:")
        traceback.print_exc()
        return jsonify({"result": f"❌ Internal error: {str(e)}"}), 500

# ✅ نقطة استقبال Webhook من Telegram
@app.route(f"/{API_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# ✅ رد على /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to Roasty FaceTo! Send me a face photo and I’ll roast it 🔥")

# ✅ رد على الصور
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    roast = "😈 That face… AI needed therapy after seeing it!"  # لاحقًا: أرسل الصورة فعليًا للذكاء الاصطناعي
    bot.reply_to(message, roast)

# ✅ رد على أي شيء آخر
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    bot.reply_to(message, "📸 Please send me a photo of a human face.")

# ✅ تشغيل التطبيق
if __name__ == "__main__":
    if BASE_URL:
        webhook_url = f"{BASE_URL}/{API_TOKEN}"
        set_hook = bot.set_webhook(url=webhook_url)
        if set_hook:
            print(f"✅ Webhook set: {webhook_url}")
        else:
            print("❌ Failed to set webhook.")
    else:
        print("⚠️ BASE_URL not set. Skipping webhook setup.")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
