from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from flask import Flask, jsonify
import frida
import threading

# --- 1. SENING ASLIY KODING (O'zgartirishsiz) ---
app = Flask(__name__)

JS_LOGIC = """
var libName = "libshadowtracker.so";
function patch() {
    var base = Module.findBaseAddress(libName);
    if (base) {
        Memory.protect(base.add(0x2B4F1A), 4, 'rwx');
        base.add(0x2B4F1A).writeByteArray([0x00, 0x00, 0x00, 0x00]);
        
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
        device = frida.get_usb_device(timeout=10)
        pid = device.spawn(["com.tencent.ig"])
        session = device.attach(pid)
        script = session.create_script(JS_LOGIC)
        script.on('message', on_message)
        script.load()
        device.resume(pid)
    except Exception as e:
        print(f"[-] Frida xatosi: {e}")

@app.route('/cgi-bin/open_crate', methods=['POST', 'GET'])
def fake_open_crate():
    return jsonify({
        "status": "SUCCESS",
        "reward_id": "m416_glacier_max", 
        "reward_type": "legendary",
        "new_balance": 999999
    })

@app.route('/account/get_balance', methods=['GET'])
def fake_balance():
    return jsonify({"uc": 999999, "ag": 999999, "status": "OK"})

# --- 2. KIVY INTERFEYSI (Androidda ko'rinishi uchun) ---
class InjectorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.lbl = Label(text="PUBG Injector Status: Ready", font_size='18sp')
        layout.add_widget(self.lbl)

        btn = Button(text="START INJECTION & SERVER", background_color=(1, 0, 0, 1), size_hint=(1, 0.4))
        btn.bind(on_press=self.run_all)
        layout.add_widget(btn)

        return layout

    def run_all(self, instance):
        # 1. Flaskni alohida oqimda yoqish
        flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False))
        flask_thread.daemon = True
        flask_thread.start()

        # 2. Fridani alohida oqimda yoqish
        frida_thread = threading.Thread(target=start_frida_logic)
        frida_thread.daemon = True
        frida_thread.start()

        self.lbl.text = "Status: Injection Started\nServer: 0.0.0.0:5000"
        instance.disabled = True
        instance.text = "RUNNING..."

if __name__ == '__main__':
    InjectorApp().run()
