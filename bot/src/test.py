# -*- coding: utf-8 -*-

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


# ボタンテンプレート
buttons_template = ButtonsTemplate(
    title="今日はどうでしたか？",
    text="回答してください",
    actions=[
        PostbackAction(label="ダメだった", data="humburger_cooking"),
        PostbackAction(label="最高だった", data="humburger_shop", text="shop"),
    ]
)

buttons_template_2 = ButtonsTemplate(
    title='この中からお選びください',
    text='Hello, my buttons',
    actions=[
        URIAction(label='Go to line.me', uri='https://line.me'),
        PostbackAction(label='ping', data='ping'),
        PostbackAction(label='ping with text', data='ping', text='ping'),
        MessageAction(label='Translate Rice', text='米')
    ]
)

# カルーセルテンプレート
carousel_template = CarouselTemplate(
    columns=[
        CarouselColumn(
            text='hoge1',
            title='fuga1',
            actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping')
            ]
        ),
        CarouselColumn(
            text='hoge2',
            title='fuga2',
            actions=[
                PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ]
        ),
    ]
)

# ビデオ

video_message = VideoSendMessage(
    original_content_url = "https://s3-ap-northeast-1.amazonaws.com/shogi-movie-bot/9ae62c26a2855cadfa103b955df9665065ace84454618b71378731bcaeff6b0e.mp4",
    preview_image_url = "https://pbs.twimg.com/profile_images/885870202738561024/U2_xyYRC_400x400.jpg"
)


def push_template_message(template):
    
    message = TemplateSendMessage(
        alt_text='Buttons alt text',
        template=template
    )

    line_bot_api.push_message(nohara_first_id, message)

def push_text_message(text):
    message = TextSendMessage(text="おっす")
    line_bot_api.push_message(nohara_first_id, message)


def template_to_message(template):

    message = TemplateSendMessage(
        alt_text = "Buttons alt text",
        template=template
    )
    return message



def sample_push():

    messages = []

    # テンプレート
    buttons_template = ButtonsTemplate(
        title="今日はどうでしたか？",
        text="回答してください",
        actions=[
            PostbackAction(label="ダメだった", data="humburger_cooking"),
            PostbackAction(label="最高だった", data="humburger_shop", text="shop"),
        ]
    )
    # 送信用にラップ
    message_buttons = template_to_message(buttons_template)
    # テキストメッセージはそのまま
    message_text = TextSendMessage(text="おっす")

    messages.append(message_buttons)
    messages.append(message_text)
    
    for m in messages:
        line_bot_api.push_message(nohara_first_id, m)