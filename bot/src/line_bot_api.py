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