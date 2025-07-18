from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import telebot
import os

# التوكن الخاص بالبوت من BotFather
API_TOKEN = os.environ.get("BOT_TOKEN")  # ضعه في إعدادات Railway كـ Environment Variable
bot = telebot.TeleBot(API_TOKEN)
if not API_TOKEN:
    raise ValueError("❌ BOT_TOKEN is missing. Please set it in environment variables.")

# إنشاء تطبيق Flask
app = Flask(__name__)
CORS(app)  # للسماح بالاتصال من Vercel

# نقطة التشغيل الرئيسية لتأكيد عمل السيرفر
@app.route("/")
def index():
    return "✅ RoastyFaceTo AI backend is running."

# نقطة استقبال الصور من الواجهة
@app.route("/roast", methods=["POST"])
def roast_image():
    if "image" not in request.files:
        return jsonify({"result": "❌ No image received."}), 400

    image_file = request.files["image"]

    try:
        # فتح الصورة للتحقق
        image = Image.open(image_file.stream)

        # 🧠 مكان إدراج نموذج الذكاء الاصطناعي لاحقًا (تعديل السطر التالي)
        roast_text = "🔥 That face could scare a mirror! 😂"

        return jsonify({"result": roast_text})
    except Exception as e:
        return jsonify({"result": f"❌ Failed to process image: {str(e)}"}), 500

# نقطة تلقي رسائل تيليجرام
@app.route(f"/{API_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# الرد على /start من المستخدم
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to Roasty FaceTo! Send me a face photo and I’ll roast it 🔥")

# الرد على الصور فقط
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    roast = "😈 That face… AI needed therapy after seeing it!"  # استبدل بـ API لو أردت
    bot.reply_to(message, roast)

# الرد على أي شيء آخر
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    bot.reply_to(message, "📸 Please send me a photo of a human face.")

# تشغيل التطبيق
if __name__ == "__main__":
    BASE_URL = os.environ.get("BASE_URL")  # أدخل من Railway

    if BASE_URL:
        webhook_url = f"{BASE_URL}/{API_TOKEN}"
        set_hook = bot.set_webhook(url=webhook_url)
        if set_hook:
            print(f"✅ Webhook set successfully: {webhook_url}")
        else:
            print("❌ Failed to set webhook.")
    else:
        print("⚠️ BASE_URL not set. Skipping webhook setup.")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

