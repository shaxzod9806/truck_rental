from motochas.celery import app
import requests


@app.task
def move_renter():
    url = "https://api.telegram.org/bot5222427534:AAHtRQkuS6dGyhesgTyq5YXI8zuncQAXcc0/sendMessage?chat_id=" \
          "516270172&text=Celery"
    r = requests.get(url)
    print(r.json())