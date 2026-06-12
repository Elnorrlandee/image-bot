import telebot
import os
from telebot import types

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN is not set in environment variables!")

bot = telebot.TeleBot(TOKEN)

def enhance_prompt(user_prompt):
    prompt = user_prompt.strip()
    
    base = "ultra realistic cinematic photo, 8K, HDR, photorealistic, highly detailed, sharp focus, intricate details, masterpiece, best quality"
    
    enhanced = f"{base}, {prompt}, professional photography, dramatic lighting, depth of field, moody atmosphere, volumetric lighting, cinematic composition"
    
    if len(prompt) < 40:
        enhanced += ", golden hour lighting, epic wide shot, 85mm lens, f/1.8 aperture, award winning photography"
    
    return enhanced

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 
        "👋 مرحباً! أنا بوت توليد برومبتات الصور بالذكاء الاصطناعي.\n\n"
        "أرسل لي أي وصف لصورة (بالعربي أو الإنجليزي) وسأحوله إلى برومبت محسن واحترافي.\n\n"
        "✅ يدعم +18 بدون قيود\n"
        "مثال: قطة ترتدي بدلة فضائية على سطح المريخ"
    )

@bot.message_handler(func=lambda message: True)
def handle_prompt(message):
    try:
        enhanced = enhance_prompt(message.text)
        
        bot.send_message(
            message.chat.id, 
            f"**✅ الـ Prompt المحسن:**\n\n{enhanced}\n\n"
            "انسخ هذا البرومبت واستخدمه في Grok, Flux, Midjourney, أو Stable Diffusion",
            parse_mode="Markdown"
        )
        
        # زر اختياري
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 توليد برومبت جديد", callback_data="new"))
        bot.send_message(message.chat.id, "هل تريد برومبت آخر؟", reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(message, "❌ حدث خطأ أثناء معالجة طلبك.")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "new":
        bot.answer_callback_query(call.id, "أرسل وصف الصورة الجديدة")

print("🤖 البوت يعمل بنجاح...")
bot.infinity_polling()