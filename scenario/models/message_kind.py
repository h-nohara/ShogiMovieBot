from django.db import models


class MessageKind(models.Model):

    '''
    text, image, movie, buttons
    '''

    class Meta:
        db_table = "message_kinds"

    title = models.CharField(
        verbose_name = "title",
        max_length = 1000,
        null = True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
