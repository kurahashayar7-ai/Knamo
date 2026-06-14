#!/bin/bash

echo "🔄 خەریکی ئەپدێدکردنی پاکێجەکانی Termux..."
pkg update -y && pkg upgrade -y

echo "📦 خەریکی دامەزراندنی پایتۆن و فلاسك و termux-api..."
pkg install python termux-api -y
pip install flask requests

echo "📝 خەریکی دروستکردنی فایلی سێرڤەر (server.py)..."
cat << 'EOF' > server.py
import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "سێرڤەری VIP HACKI BRAIAN بە سەرکەوتوویی کار دەکات!"

@app.route('/set_volume', methods=['GET'])
def set_volume():
    level = request.args.get('level', default='3', type=str)
    try:
        command = f"termux-volume music {level}"
        subprocess.run(command, shell=True, check=True)
        return jsonify({"status": "success", "message": f"دەنگ گۆڕدرا بۆ {level}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

EOF

echo "🚀 هەموو شتێک ئامادەیە! ئێستا سێرڤەرەکە دەکرێتەوە..."
python server.py

