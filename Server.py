import os
import subprocess
import json
import base64
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>کۆنتڕۆڵی مۆبایل</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #1a1a2e; color: white; }
        button { padding: 15px; margin: 5px; background: #00d4ff; border: none; color: #1a1a2e; border-radius: 10px; cursor: pointer; }
        input { padding: 10px; margin: 5px; border-radius: 10px; }
        .card { background: #16213e; padding: 15px; margin: 10px 0; border-radius: 15px; }
        .status { background: #0f3460; padding: 10px; margin-top: 10px; border-radius: 10px; }
    </style>
</head>
<body>
<h1>📱 کۆنتڕۆڵی مۆبایل</h1>

<div class="card">
    <h3>🔊 دەنگ</h3>
    <button onclick="cmd('volume',0)">🔇 0</button>
    <button onclick="cmd('volume',5)">🔉 5</button>
    <button onclick="cmd('volume',10)">🔊 10</button>
    <button onclick="cmd('volume',15)">📢 15</button>
</div>

<div class="card">
    <h3>📱 کۆنتڕۆڵ</h3>
    <button onclick="cmd('home')">🏠 هۆم</button>
    <button onclick="cmd('back')">🔙 گەڕانەوە</button>
    <button onclick="cmd('recents')">📋 دوایینەکان</button>
    <button onclick="cmd('lock')">🔒 قوفڵ</button>
</div>

<div class="card">
    <h3>⌨️ ناردنی دەق</h3>
    <input type="text" id="text" placeholder="دەقێک بنووسە...">
    <button onclick="sendText()">📝 ناردن</button>
</div>

<div class="card">
    <h3>ℹ️ زانیاری</h3>
    <button onclick="getBattery()">🔋 باتری</button>
    <button onclick="getInfo()">📱 زانیاری</button>
    <div id="info" class="status"></div>
</div>

<script>
async function cmd(action, value=null) {
    let url = '/cmd/' + action;
    if(value) url += '?value=' + value;
    try {
        let r = await fetch(url);
        let d = await r.json();
        document.getElementById('info').innerHTML = '✅ ' + d.message;
        setTimeout(()=>{ if(document.getElementById('info').innerHTML.includes('✅')) document.getElementById('info').innerHTML = ''; },2000);
    } catch(e) {
        document.getElementById('info').innerHTML = '❌ ' + e.message;
    }
}

async function sendText() {
    let text = document.getElementById('text').value;
    if(text) await cmd('type', text);
}

async function getBattery() {
    let r = await fetch('/battery');
    let d = await r.json();
    document.getElementById('info').innerHTML = '🔋 ' + d.message;
}

async function getInfo() {
    let r = await fetch('/info');
    let d = await r.json();
    document.getElementById('info').innerHTML = '📱 ' + d.message;
}
</script>
</body>
</html>
'''

def run_termux_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/cmd/<action>')
def do_cmd(action):
    value = request.args.get('value', '')
    
    # دەنگ
    if action == 'volume':
        os.system(f'termux-volume music {value}')
        return jsonify({'message': f'دەنگ گۆڕا بۆ {value}'})
    
    # ناردنی دەق
    elif action == 'type':
        os.system(f'input text "{value}"')
        return jsonify({'message': f'دەق "{value}" نێردرا'})
    
    # کۆنتڕۆڵەکان
    elif action == 'home':
        os.system('input keyevent KEYCODE_HOME')
    elif action == 'back':
        os.system('input keyevent KEYCODE_BACK')
    elif action == 'recents':
        os.system('input keyevent KEYCODE_APP_SWITCH')
    elif action == 'lock':
        os.system('input keyevent KEYCODE_POWER')
    elif action == 'unlock':
        os.system('input keyevent KEYCODE_POWER')
    elif action == 'volume_up':
        os.system('input keyevent KEYCODE_VOLUME_UP')
    elif action == 'volume_down':
        os.system('input keyevent KEYCODE_VOLUME_DOWN')
    
    return jsonify({'message': f'فرمان {action} جێبەجێ کرا'})

@app.route('/battery')
def get_battery():
    try:
        result = subprocess.getoutput('termux-battery-status')
        data = json.loads(result)
        return jsonify({'message': f"{data.get('percentage', '?')}% - {data.get('status', 'نادیار')}"})
    except:
        return jsonify({'message': 'نەتوانرا بارستەی باتری بهێنرێت'})

@app.route('/info')
def get_info():
    result = subprocess.getoutput('termux-info | head -5')
    return jsonify({'message': result.replace('\n', ' ')[:100]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
