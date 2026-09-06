import os
import threading
import requests
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
  return "Bot aktif ve çalışıyor!"


def run_bot():
  # Render'a kaydettiğimiz gizli Lichess token'ını alıyoruz
  token = os.environ.get("LICHESS_TOKEN")

  if not token:
    print("HATA: LICHESS_TOKEN bulunamadı!")
    return

  headers = {"Authorization": f"Bearer {token}"}

  print("Lichess'e bağlanılıyor...")

  try:
    # Botun Lichess hesabına bağlanıp bağlanamadığını test ediyoruz
    response = requests.get("https://lichess.org/api/account", headers=headers)
    if response.status_code == 200:
      user_data = response.json()
      print(f"BAŞARILI! Bot Lichess'e bağlandı. Kullanıcı adı: {user_data.get('username')}")
    else:
      print(f"Bağlantı başarısız! Kod: {response.status_code}, Mesaj: {response.text}")
  except Exception as e:
    print(f"Bir hata oluştu: {e}")


if __name__ == "__main__":
  # Botu arka planda çalıştıracak thread'i başlatıyoruz
  bot_thread = threading.Thread(target=run_bot)
  bot_thread.start()

  # Render'ın çökmemesi için gereken web sunucusunu başlatıyoruz
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
