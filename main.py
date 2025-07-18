from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import telebot
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
    if "image" not in request.files:
        return jsonify({"result": "❌ No image received."}), 400

    image_file = request.files["image"]

    try:
        # فتح الصورة (يمكنك مستقبلاً إرسالها إلى API خارجي هنا)
        image = Image.open(image_file.stream)

        # 🧠 رد ذكي مبدئي — عدّله لاحقًا حسب الذكاء الاصطناعي
        roast_text = "🔥 That face could scare a mirror! 😂"

        return jsonify({"result": roast_text})
    except Exception as e:
        return jsonify({"result": f"❌ Failed to process image: {str(e)}"}), 500

# ✅ نقطة استقبال Webhook من Telegram
@app.route(f"/{API_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])

