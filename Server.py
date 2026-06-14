#!/bin/bash
clear
echo "🔄 خەریکی ئەپدێدکردنی سیستەم و دامەزراندنی پێداویستییەکان..."
pkg update -y && pkg upgrade -y
pkg install python termux-api git -y
pip install pyTelegramBotAPI

echo "-------------------------------------------"
echo "🤖 تکایە تۆکنی بۆتی تێلێگرامەکەت (Bot Token) لێرە دابنێ:"
read -p "Token: " USER_TOKEN
echo "-------------------------------------------"

# گۆڕینی تۆکنەکە لە ناو فایلی پایتۆنەکەدا
sed -i "s/8654377707:AAHxypvl3zUl0HvSKgfEyWWeYNc9KAp1iMQ/$USER_TOKEN/g" bot.py

echo "🚀 هەموو شتێک ئامادەیە! بۆتەکە ئێستا چالاک بوو..."
python bot.py
