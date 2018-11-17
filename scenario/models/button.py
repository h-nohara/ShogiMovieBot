from django.db import models

# db
from scenario.models.message import Message

class Button(models.Model):

    '''
    ボタンメッセージに紐づくボタン
    '''

    class Meta:
        db_table = "buttons"

    message = models.ForeignKey(
        Message,
        related_name = 'buttons',
        on_delete = models.SET_NULL,
        null = True
    )

    text = models.CharField(
        verbose_name = "text",
        max_length = 1000,
        null = True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
