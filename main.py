from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from flask import Flask, jsonify
import threading
import random
import socket

# --- 1. FAKE SERVER LOGIKASI (O'yinni aldash uchun) ---
app = Flask(__name__)

@app.route('/cgi-bin/open_crate', methods=['POST', 'GET'])
def fake_open_crate():
    # Real o'yin shansi (Ehtimolliklar)
    items = [
        {"id": "silver_01", "name": "Silver Coin", "type": "rare", "weight": 70},
        {"id": "outfit_05", "name": "School Shoes", "type": "rare", "weight": 20},
        {"id": "m416_glacier", "name": "M416 Glacier", "type": "mythic", "weight": 1}, # 1% OMAD!
        {"id": "coupon_01", "name": "Classic Coupon", "type": "epic", "weight": 9}
    ]
    
    # Tasodifiy buyumni tanlash
    reward = random.choices(items, weights=[i['weight'] for i in items], k=1)[0]
    
    return jsonify({
        "status": "SUCCESS",
        "reward_id": reward['id'],
        "reward_name": reward['name'],
        "reward_type": reward['type'],
        "new_balance": 999999,
        "message": "Item obtained successfully!"
    })

@app.route('/account/get_balance', methods=['GET'])
def fake_balance():
    return jsonify({
        "uc": 999999,
        "ag": 999999,
        "bp": 9999999,
        "status": "OK"
    })

def run_server():
    # host='0.0.0.0' o'yin senga ulanishi uchun shart
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# --- 2. ANDROID INTERFEYSI (Kivy) ---
class PUBG_Injector(App):
    def build(self):
        # Oyna rangini qora qilamiz
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        
        # Sarlavha
        self.status_lbl = Label(
            text="PUBG PREMIM INJECTOR\n(Server Mode)", 
            font_size='25sp', 
            halign="center",
            color=(1, 0.8, 0, 1) # Oltin rang
        )
        layout.add_widget(self.status_lbl)

        # Ma'lumot
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "127.0.0.1"

        self.info_lbl = Label(
            text=f"Server IP: {local_ip}\nUC: 999,999\nStatus: Offline",
            font_size='18sp',
            halign="center"
        )
        layout.add_widget(self.info_lbl)

        # Tugma
        self.btn = Button(
            text="SERVERNI ISHGA TUSHIRISH",
            size_hint=(1, 0.4),
            background_color=(0, 0.5, 0.8, 1),
            font_size='20sp'
        )
        self.btn.bind(on_press=self.start_all)
        layout.add_widget(self.btn)

        return layout

    def start_all(self, instance):
        # Flask serverni fon oqimida ishga tushirish
        threading.Thread(target=run_server, daemon=True).start()
        
        self.status_lbl.text = "INJECTOR: ACTIVE"
        self.info_lbl.text = "Status: Online (5000 port)\nKeys ochishga tayyor!"
        self.info_lbl.color = (0, 1, 0, 1) # Yashil rang
        
        instance.text = "SERVER ISHLAYAPTI"
        instance.disabled = True
        instance.background_color = (0.3, 0.3, 0.3, 1)

if __name__ == '__main__':
    PUBG_Injector().run()
