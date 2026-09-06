import os
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif!"

# Botunun asıl kodunu (Lichess bağlantı kısmı) buraya ekleyebilirsin
def run_bot():
    # Buraya normal bot başlatma kodunu yazıyorsun
    print("Bot başlatılıyor...")

if __name__ == "__main__":
    # Botu arka planda çalıştır
    t = threading.Thread(target=run_bot)
    t.start()
    
    # Render'ın istediği web sunucusunu başlat
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
