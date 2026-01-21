from flask import Flask, render_template, jsonify
import frida
import sys
import os
import threading

app = Flask(__name__)

# --- SENING KODING (O'ZGARTIRILMADI) ---
JS_LOGIC = """
var libName = "libshadowtracker.so";
function patch() {
    var base = Module.findBaseAddress(libName);
    if (base) {
        // Price Nulling (0x2B4F1A)
        Memory.protect(base.add(0x2B4F1A), 4, 'rwx');
        base.add(0x2B4F1A).writeByteArray([0x00, 0x00, 0x00, 0x00]);
        
        // Success Bypass (0x6A1B22)
        Memory.protect(base.add(0x6A1B22), 4, 'rwx');
        base.add(0x6A1B22).writeByteArray([0x01, 0x00, 0xA0, 0xE3]);
        send("SUCCESS");
    } else { setTimeout(patch, 1000); }
}
patch();
"""

def on_message(msg, data):
    if msg['type'] == 'send': print(f"[*] Signal: {msg['payload']}")

def start_frida_logic():
    try:
        device = frida.get_usb_device(timeout=10)
        pid = device.spawn(["com.tencent.ig"])
        session = device.attach(pid)
        script = session.create_script(JS_LOGIC)
        script.on('message', on_message)
        script.load()
        device.resume(pid)
        # sys.stdin.read() olib tashlandi, chunki u serverni bloklab qo'yadi
    except Exception as e:
        print(f"Xato: {e}")
# --- SENING KODING TUGADI ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_injection', methods=['POST'])
def run_injection():
    # Injektsiyani alohida oqimda (thread) ishga tushiramiz
    thread = threading.Thread(target=start_frida_logic)
    thread.start()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)