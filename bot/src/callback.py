import os, sys, json

# api
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# line bot
# from .line_bot_api import line_bot_api, handler
# from .line_bot_api import *

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, VideoSendMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)


nohara_first_id = "U553c96922aa681d777bb5f97b2b8f99f"

CHANNEL_ACCESS_TOKEN = "NR7wgVMEMdyipWrLr06dAXmvlu7C7leBlU2Eb+dOHY6HjjQz5Ukav9l4ZDpf6nVJreL468xmCZuHpxK02JRvK2Q0hFZZjAThYU+f4q0tu7vQkaB4QyhQfNomL3NEx0Himm4YJxbWHLpRKLk+TCyjuQdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "4e128a5ebac89175f69af88f9715bc7a"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@csrf_exempt
def callback(request):

    '''
    {
        "data" : {
            "text" : "hoge"
        }
    }
    '''
    
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    data = data["data"]
    text = data["text"]

    # token = data["token"]
    # line_bot_api.reply_message(token, TextSendMessage(text=text))

    push_text_message("おうむ返し:" + text)

    if text == "棋譜":
        pass

    return "ok"


def push_template_message(template):
    
    message = TemplateSendMessage(
        alt_text='Buttons alt text',
        template=template
    )

    line_bot_api.push_message(nohara_first_id, message)

def push_text_message(text):
    message = TextSendMessage(text=text)
    line_bot_api.push_message(nohara_first_id, message)


def template_to_message(template):

    message = TemplateSendMessage(
        alt_text = "Buttons alt text",
        template=template
    )
    return message



# @csrf_exempt
# def callback(request):

#     print("receive callback")

#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = request.get_data(as_text=True)

#     # handle webhook body
#     try:
#         print("ok")
#         handler.handle(body, signature)

#     except InvalidSignatureError:
#         print("oh no")
#         abort(400)



# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):

#     print("receive message event")
    
#     text_receive = event.message.text

#     # おうむ返し
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=text_receive)
#     )