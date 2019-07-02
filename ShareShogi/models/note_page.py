from django.db import models

# db
from accounts.models.user import User
from ShareShogi.models.note import Note

class NotePage(models.Model):

    class Meta:
        db_table = "note pages"

    note = models.ForeignKey(
        Note,
        related_name = 'note_pages',
        on_delete = models.SET_NULL,
        null = True
    )

    message = models.CharField(
        verbose_name = "message",
        max_length = 1000,
        null = True
    )

    image_url = models.CharField(
        verbose_name = "image",
        max_length = 1000,
        null = True
    )

    order_in_parent = models.IntegerField(
        verbose_name = "order",
        default = 0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    