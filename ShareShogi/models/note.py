from django.db import models

# db
from accounts.models.user import User

class Note(models.Model):

    class Meta:
        db_table = "notes"

    user = models.ForeignKey(
        User,
        related_name = 'notes',
        on_delete = models.SET_NULL,
        null = True
    )

    title = models.CharField(
        verbose_name = "title",
        max_length = 1000,
        null = True
    )

    thumb_url = models.CharField(
        verbose_name = "thumb",
        max_length = 1000,
        null = True
    )

    opening_sente = models.CharField(
        verbose_name = "opening_sente",
        max_length = 1000,
        null = True
    )

    opening_gote = models.CharField(
        verbose_name = "opening_gote",
        max_length = 1000,
        null = True
    )

    is_public = models.BooleanField(
        verbose_name = "public or not",
        default = False
    )

    favo = models.IntegerField(
        verbose_name = "favo",
        default = 0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    