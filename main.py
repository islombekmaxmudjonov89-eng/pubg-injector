from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from flask import Flask, jsonify
import threading
import socket

# --- 1. Sening FAKE SERVER logikang ---
app = Flask(__name__)

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

def run_flask():
    # host='0.0.0.0' bu juda muhim, shunda o'yin senga ulana oladi
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# --- 2. KIVY INTERFEYSI ---
class InjectorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # IP manzilni aniqlash (O'yinni senga yo'naltirish uchun kerak)
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        self.lbl = Label(text=f"Server IP: {local_ip}\nPort: 5000\nHolat: Tayyor", 
                         font_size='18sp', halign="center")
        layout.add_widget(self.lbl)

        btn = Button(text="SERVERNI ISHGA TUSHIRISH", 
                     background_color=(0, 0.7, 1, 1), 
                     size_hint=(1, 0.4))
        btn.bind(on_press=self.start_server)
        layout.add_widget(btn)

        return layout

    def start_server(self, instance):
        threading.Thread(target=run_flask, daemon=True).start()
        self.lbl.text = "STATUS: SERVER ISHLAYAPTI\nO'yin so'rovlarini kutmoqda..."
        instance.text = "SERVER ON"
        instance.disabled = True

if __name__ == '__main__':
    InjectorApp().run()
