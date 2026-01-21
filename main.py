from flask import Flask, render_template, jsonify, request
import frida
import threading
import os

app = Flask(__name__)

# --- 1. FRIDA JS LOGIC (Xotira manzillarini patch qilish) ---
JS_LOGIC = """
var libName = "libshadowtracker.so";
function patch() {
    var base = Module.findBaseAddress(libName);
    if (base) {
        // Price Nulling (Keys narxini 0 qilish)
        Memory.protect(base.add(0x2B4F1A), 4, 'rwx');
        base.add(0x2B4F1A).writeByteArray([0x00, 0x00, 0x00, 0x00]);
        
        // Success Bypass (Server javobini kutmasdan tasdiqlash)
        Memory.protect(base.add(0x6A1B22), 4, 'rwx');
        base.add(0x6A1B22).writeByteArray([0x01, 0x00, 0xA0, 0xE3]);
        send({type: 'info', payload: 'MEM_PATCHED'});
    } else { 
        setTimeout(patch, 1000); 
    }
}
patch();
"""

def on_message(msg, data):
    if msg['type'] == 'send':
        print(f"[*] Signal: {msg['payload']}")

def start_frida_logic():
    try:
        # USB orqali ulangan qurilmani topish (emulator yoki telefon)
        device = frida.get_usb_device(timeout=10)
        # O'yinni yangidan ishga tushirish (spawn)
        pid = device.spawn(["com.tencent.ig"])
        session = device.attach(pid)
        script = session.create_script(JS_LOGIC)
        script.on('message', on_message)
        script.load()
        device.resume(pid)
        print("[*] Injektsiya va Patch muvaffaqiyatli!")
    except Exception as e:
        print(f"[-] Frida xatosi: {e}")

# --- 2. FAKE SERVER ROUTES (Keys ochishni aldash) ---

@app.route('/')
def index():
    return render_template('index.html')

# Keys ochish so'rovini tutib qolish (Taxminiy URL)
@app.route('/cgi-bin/open_crate', methods=['POST', 'GET'])
def fake_open_crate():
    # O'yin keys ochmoqchi bo'lganda sening servering SUCCESS qaytaradi
    return jsonify({
        "status": "SUCCESS",
        "reward_id": "m416_glacier_max", 
        "reward_type": "legendary",
        "new_balance": 999999
    })

# Balansni tekshirish so'rovini tutib qolish
@app.route('/account/get_balance', methods=['GET'])
def fake_balance():
    return jsonify({
        "uc": 999999,
        "ag": 999999,
        "status": "OK"
    })

@app.route('/run_injection', methods=['POST'])
def run_injection():
    # Injektsiyani alohida oqimda ishga tushiramiz
    t = threading.Thread(target=start_frida_logic)
    t.daemon = True
    t.start()
    return jsonify({"status": "Injection started", "server": "Running"})

if __name__ == '__main__':
    # host='0.0.0.0' orqali o'yin sening serveringga ulanishi mumkin bo'ladi
    app.run(host='0.0.0.0', port=5000, debug=False)
