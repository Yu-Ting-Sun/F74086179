import os

from linebot import LineBotApi, WebhookParser
from linebot.models import  CarouselTemplate,CarouselColumn,MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, URITemplateAction, ButtonsTemplate, MessageTemplateAction, ImageSendMessage

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_text_message_AI(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token,TextSendMessage(text=Olami().nli(text)))

    return "OK"

def send_carousel_message(reply_token, col):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = ImageCarouselTemplate(columns = col)
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_button_message(reply_token, title, text, btn, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_image_and_text_message(reply_token, url,text):
    line_bot_api = LineBotApi(channel_access_token) 
    message1 = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    message2 = TextSendMessage(text=text)
    message = [message1,message2]
    line_bot_api.reply_message(reply_token, message)

    return "OK"    


def send_button_carousel(reply_token, col):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(columns = col)
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_multi_image(reply_token, url1,url2,url3,url4):
    line_bot_api = LineBotApi(channel_access_token) 
    message1 = ImageSendMessage(
        original_content_url = url1,
        preview_image_url = url1
    )
    message2 = ImageSendMessage(
        original_content_url = url2,
        preview_image_url = url2
    )
    message3 = ImageSendMessage(
        original_content_url = url3,
        preview_image_url = url3
    )
    message4 = ImageSendMessage(
        original_content_url = url4,
        preview_image_url = url4
    )        
    message = [message1,message2,message3,message4]
    line_bot_api.reply_message(reply_token, message)

    return "OK"    