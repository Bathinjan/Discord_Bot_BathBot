# Web Server with continuous ping to ensure constant uptime

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Awake."

def run():
  app.run(host='0.0.0.0', port = 8080)

def keep_awake():
  t = Thread(target = run)
  t.start()
