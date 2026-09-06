import json
import os
import threading
import time
import requests
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
  return "Bot aktif ve çalışıyor!"


def run_bot():
  token = os.environ.get("LICHESS_TOKEN")
  if not token:
    print("HATA: LICHESS_TOKEN bulunamadı!")
    return

  headers = {"Authorization": f"Bearer {token}"}
  print("Lichess etkinlik akışına bağlanılıyor...")

  while True:
    try:
      # Lichess event stream botu sürekli çevrimiçi tutar ve gelen maçları dinler
      response = requests.get(
          "https://lichess.org/api/stream/event", headers=headers, stream=True
      )
      if response.status_code == 200:
        print("BAŞARILI: Bot Lichess'e bağlandı ve çevrimiçi!")
        for line in response.iter_lines():
          if line:
            event = json.loads(line.decode("utf-8"))
            print(f"Gelen olay: {event}")
            # Buraya ileride maç kabul etme kodları eklenebilir
      else:
        print(
            f"Bağlantı hatası! Kod: {response.status_code}, Mesaj:"
            f" {response.text}"
        )
    except Exception as e:
      print(f"Bağlantı koptu: {e}")

    # Kopma olursa 5 saniye bekleyip tekrar bağlanmayı dener
    time.sleep(5)


if __name__ == "__main__":
  bot_thread = threading.Thread(target=run_bot)
  bot_thread.start()

  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
