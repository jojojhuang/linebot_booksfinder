from flask import request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)
from linebot_booksfinder import app, line_bot_api, handler
from linebot_booksfinder.msg_templates import (
    generate_carousel_for_search, generate_search_bubble_from_key, generate_carousel_for_top10
)
from linebot_booksfinder.util.bookspider import crawl_books_by_key, crawl_top10

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text == '@排行' or text.lower() == '@rank':
        send_top10_message(event)
    else:
        send_search_result_message(event)

def send_top10_message(event):
    books = crawl_top10()
    msg   = []

    try:
        carousel = generate_carousel_for_top10(books)
        msg.append(
            FlexSendMessage(
                alt_text = '排行榜前10名',
                contents = carousel
            )
        )
    except Exception:
        msg.append(
            TextSendMessage(text='發生錯誤，請稍候再試')
        )
    
    line_bot_api.reply_message(event.reply_token, msg)


def send_search_result_message(event):
    # 透過關鍵字取得書籍
    # CarouselContainer 最多只能包含10個 BubbleContainer
    key   = event.message.text
    books = crawl_books_by_key(key, result_max=10)
    msg   = []

    if len(books) == 0:
        msg.append(
            TextSendMessage(text='沒有符合 {} 的查詢結果'.format(key))
        )
    else:
        carousel = generate_carousel_for_search(books)
        msg.append(
            FlexSendMessage(
                alt_text = '{0} 的前{1}個查詢結果'.format(key, len(books)),
                contents = carousel
            )
        )
        search_bubble = generate_search_bubble_from_key(key)
        msg.append(
            FlexSendMessage(
                alt_text = '更多 {} 的搜尋結果'.format(key),
                contents = search_bubble
            )
        )        
    
    line_bot_api.reply_message(event.reply_token, msg)