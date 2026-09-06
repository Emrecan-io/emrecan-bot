import json
import os
import threading
import time
import requests
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
  return "Bot aktif!"


def run_bot():
  token = os.environ.get("LICHESS_TOKEN")
  if not token:
    print("LICHESS_TOKEN bulunamadı!")
    return

  headers = {"Authorization": f"Bearer {token}"}
  print("Bot Lichess'e bağlanıyor...")

  while True:
    try:
      response = requests.get(
          "https://lichess.org/api/stream/event", headers=headers, stream=True
      )
      if response.status_code == 200:
        print("BAŞARILI: Bot Lichess'e bağlandı ve çevrimiçi!")
        for line in response.iter_lines():
          if line:
            event = json.loads(line.decode("utf-8"))
            print(f"Gelen olay: {event}")
      else:
        print(f"Hata kodu: {response.status_code}")
    except Exception as e:
      print(f"Bağlantı hatası: {e}")
    time.sleep(5)


if __name__ == "__main__":
  # Botu arka planda çalıştır
  t = threading.Thread(target=run_bot)
  t.start()

  # Render'ın istediği web sunucusunu başlat (Ücretsiz kalmasını sağlar)
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
