import os, json
from flask import Flask
from linebot import LineBotApi, WebhookHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd10d2770615e33f98496300b718a28b5'

linebot_keyfile = 'config/linebotKey.json'
with open(linebot_keyfile) as key_file:
    linebotKey = json.load(key_file)

line_bot_api = LineBotApi(linebotKey['CHANNEL_ACCESS_TOKEN'])
handler      = WebhookHandler(linebotKey['CHANNEL_SECRET'])

from linebot_booksfinder import routes
