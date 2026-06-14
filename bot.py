import os
import telebot
from telebot import types
import subprocess

# ئەم بەهایە بە شێوەی ئۆتۆماتیکی لە ڕێگەی فایلی ڕێکخستنەوە دەگۆڕدرێت
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

# دروستکردنی لیستی فەرمانەکان (کیبۆردی دوگمەکان)
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_full = types.KeyboardButton("🔊 دەنگ فول (15)")
    btn_med = types.KeyboardButton("🔉 دەنگ ناوەند (7)")
    btn_low = types.KeyboardButton("🔈 دەنگ کەم (2)")
    btn_vibrate = types.KeyboardButton("📳 لێدانی ڤیبڕەیشن")
    btn_torch_on = types.KeyboardButton("🔦 داگیرساندنی فلاش")
    btn_torch_off = types.KeyboardButton("❌ کوژاندنەوەی فلاش")
    
    markup.add(btn_full, btn_med, btn_low, btn_vibrate, btn_torch_on, btn_torch_off)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = "👋 بەخێربێیت بۆ بۆتی کۆنتڕۆڵی مۆبایل!\n\n👇 فەرمانێک هەڵبژێره بۆ جێبەجێکردن لەسەر مۆبایلەکەت:"
    bot.send_message(message.chat.id, welcome_msg, reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_commands(message):
    text = message.text
    try:
        if text == "🔊 دەنگ فول (15)":
            subprocess.run("termux-volume music 15", shell=True)
            bot.reply_to(message, "✅ دەنگی مۆبایلەکە کرایە بەرزترین ئاست.")
            
        elif text == "🔉 دەنگ ناوەند (7)":
            subprocess.run("termux-volume music 7", shell=True)
            bot.reply_to(message, "✅ دەنگی مۆبایلەکە کرایە ئاستی ناوەند.")
            
        elif text == "🔈 دەنگ کەم (2)":
            subprocess.run("termux-volume music 2", shell=True)
            bot.reply_to(message, "✅ دەنگی مۆبایلەکە کەمکرایەوە.")
            
        elif text == "📳 لێدانی ڤیبڕەیشن":
            subprocess.run("termux-vibrate -d 1000", shell=True)
            bot.reply_to(message, "✅ مۆبایلەکە بۆ ١ چرکە لێی ڤیبڕەیشن دا.")
            
        elif text == "🔦 داگیرساندنی فلاش":
            subprocess.run("termux-torch on", shell=True)
            bot.reply_to(message, "✅ فلاشی مۆبایلەکە داگیرسا.")
            
        elif text == "❌ کوژاندنەوەی فلاش":
            subprocess.run("termux-torch off", shell=True)
            bot.reply_to(message, "✅ فلاشی مۆبایلەکە کوژایەوە.")
            
    except Exception as e:
        bot.reply_to(message, f"❌ کێشەیەک ڕوویدا:\n`{str(e)}`", parse_mode="Markdown")

print("🚀 بۆتی VIP HACKI BRAIAN بەبێ کێشە کای پێکرا...")
bot.infinity_polling()
