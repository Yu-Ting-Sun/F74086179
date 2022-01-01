import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,CarouselColumn

from fsm import TocMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message

load_dotenv()


machine = TocMachine(
    states=["user","intro", "hero","summary","feature","newbie","easy_hero","location","show_easy_hero","show_location","get_location",
    "free","hero_intro","show_hero_intro","test1","test2","test3","test4","test5","test6","result"],
    transitions=[
        {"trigger": "advance","source": "user","dest": "intro","conditions": "is_going_to_intro",},
        {"trigger": "advance","source": "user","dest": "hero","conditions": "is_going_to_hero",},
        {"trigger": "advance","source": "user","dest": "test1","conditions": "is_going_to_test1",},
        {"trigger": "advance","source": "test1","dest": "test2","conditions": "is_going_to_test2",},
        {"trigger": "advance","source": "test2","dest": "test3","conditions": "is_going_to_test3",},
        {"trigger": "advance","source": "test3","dest": "test4","conditions": "is_going_to_test4",},
        {"trigger": "advance","source": "test4","dest": "test5","conditions": "is_going_to_test5",},
        {"trigger": "advance","source": "test5","dest": "test6","conditions": "is_going_to_test6",},
        {"trigger": "advance","source": "test6","dest": "result","conditions": "is_going_to_result",},                                                    
        {"trigger": "advance","source": "intro","dest": "summary","conditions": "is_going_to_summary",}, 
        {"trigger": "advance","source": "intro","dest": "feature","conditions": "is_going_to_feature",},            
        {"trigger": "advance","source": "intro","dest": "newbie","conditions": "is_going_to_newbie",},
        {"trigger": "advance","source": ["summary","feature","newbie"],"dest": "intro","conditions": "is_going_to_intro",},
        {"trigger": "advance","source": "newbie","dest": "easy_hero","conditions": "is_going_to_easy_hero",},
        {"trigger": "advance","source": "newbie","dest": "location","conditions": "is_going_to_location",},
        {"trigger": "advance","source": ["location","easy_hero"],"dest": "newbie","conditions": "is_going_to_newbie",},
        {"trigger": "advance","source": "easy_hero","dest": "show_easy_hero","conditions": "is_going_to_show_easy_hero",},
        {"trigger": "advance","source": "show_easy_hero","dest": "easy_hero","conditions": "back_show_easy_hero",},
        {"trigger": "advance","source": "location","dest": "show_location","conditions": "is_going_to_show_location",},
        {"trigger": "advance","source": "show_location","dest": "get_location","conditions": "is_going_to_get_location",},
        {"trigger": "advance","source": "show_location","dest": "location","conditions": "is_going_to_location",},
        {"trigger": "advance","source": "get_location","dest": "show_location","conditions": "back_show_location",},
        {"trigger": "advance","source": "hero","dest": "free","conditions": "is_going_to_free",},    
        {"trigger": "advance","source": "hero","dest": "hero_intro","conditions": "is_going_to_hero_intro",},
        {"trigger": "advance","source": ["hero_intro","free"],"dest": "hero","conditions": "back_hero",},                                                            
        {"trigger": "advance","source": "hero_intro","dest": "show_hero_intro","conditions": "is_going_to_show_hero_intro",},
        {"trigger": "advance","source": "show_hero_intro","dest": "hero_intro","conditions": "back_hero_intro",},   
                                                                     
         
        {
            "trigger": "advance",
            "source": [
                "intro", 
                "hero",
                "test1",
                "test2",
                "test3",
                "test4",
                "test5",
                "test6",
                "result",
                "summary",
                "feature",
                "newbie",
                "easy_hero",
                "location",
                "show_location",
                "show_easy_hero",
                "get_location",
                "free",
                "hero_intro",
                "show_hero_intro"
                ], 
            "dest": "user",
            "conditions": "is_going_to_user",
        },        
        
        # {
        #     "trigger": "go_back", 
        #     "source": [
        #         "intro", 
        #         "hero"
        #         ], 
        #         "dest": "user"
        # },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        
        
        response = machine.advance(event)
        if response == False:
            if machine.state != 'user' and event.message.text.lower() == 'restart':
                send_text_message(event.reply_token, '你好！我是你的傳說小助理\n' + 
        '輸入『介紹』可查看遊戲相關介紹\n' + '輸入『英雄』可查看英雄相關資訊\n' + '輸入『檢測適合位置』可檢測你適合玩的位置\n' + 
        '隨時輸入『back』可以回到上一頁\n隨時輸入『restart』可以從頭開始。' )
                machine.go_back(event)             
            elif machine.state == 'user':
                send_text_message(event.reply_token, '你好！我是你的傳說小助理\n' + 
        '輸入『介紹』可查看遊戲相關介紹\n' + '輸入『英雄』可查看英雄相關資訊\n' + '輸入『檢測適合位置』可檢測你適合玩的位置\n' + 
        '隨時輸入『back』可以回到上一頁\n隨時輸入『restart』可以從頭開始。' )
              
            elif machine.state == 'hero':
                send_text_message(event.reply_token, '請輸入你想查看的英雄')
            elif machine.state == 'intro':
                send_text_message(event.reply_token, '請選擇你想知道的資訊')
            elif machine.state == 'summary':
                send_text_message(event.reply_token, '輸入『back』可以回到上一頁，隨時輸入『restart』可以從頭開始')
            elif machine.state == 'feature':
                send_text_message(event.reply_token, '輸入『back』可以回到上一頁，隨時輸入『restart』可以從頭開始')
            elif machine.state == 'hero_intro':
                send_text_message(event.reply_token, '請輸入整數1~103')                                                     
                             

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
