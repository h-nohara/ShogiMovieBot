from django.db import models

# db
from scenario.models.scenario import Scenario
from scenario.models.scenario_kind import MessageKind

class Message(models.Model):

    class Meta:
        db_table = "messages"

    scenario = models.ForeignKey(
        Scenario,
        related_name = 'messages',
        on_delete = models.SET_NULL,
        null = True
    )

    message_kind = models.ForeignKey(
        MessageKind,
        related_name = 'messages',
        on_delete = models.SET_NULL,
        null = True
    )

    stop = models.BooleanField(
        verbose_name = "stop here or not",
        default = False,
    )

    # テキストメッセージ用
    text = models.CharField(
        verbose_name = "text(text_message)",
        max_length = 1000,
        null = True
    )

    # 動画メッセージ用
    image_path = models.CharField(
        verbose_name = "image_path",
        max_length = 1000,
        null = True
    )

    # 動画メッセージ用
    movie_path = models.CharField(
        verbose_name = "movie_path",
        max_length = 1000,
        null = True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
