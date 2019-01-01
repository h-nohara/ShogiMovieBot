from django.db import models
from bot.models.scenario import Scenario


class Message(models.Model):

    class Meta:
        db_table = "messages"

    scenario = models.ForeignKey(
        Scenario,
        related_name = 'messages',
        on_delete = models.SET_NULL,
        null = True
    )

    kind = models.CharField(
        verbose_name = "kind",
        max_length = 1000,
        null = True
    )

    # テキストメッセージ用
    text = models.CharField(
        verbose_name = "text",
        max_length = 1000,
        null = True
    )

    # 画像メッセージ用
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

    # シナリオを一旦ここでストップするかどうか
    is_stop = models.BooleanField(
        verbose_name = "stop here or not",
        default = False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    