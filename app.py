import json
import os
import time
import requests

print("Lichess Bot başlatılıyor...")

token = os.environ.get("LICHESS_TOKEN")
if not token:
  print("HATA: LICHESS_TOKEN bulunamadı!")
  exit(1)

headers = {"Authorization": f"Bearer {token}"}

while True:
  try:
    print("Lichess etkinlik akışına bağlanılıyor...")
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
      print(
          f"Bağlantı hatası! Kod: {response.status_code}, Mesaj:"
          f" {response.text}"
      )

  except Exception as e:
    print(f"Bağlantı sırasında bir hata oluştu: {e}")

  print("Bağlantı koptu, 5 saniye sonra tekrar deneniyor...")
  time.sleep(5)
