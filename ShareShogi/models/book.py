from django.db import models

# db
from accounts.models.user import User

class Book(models.Model):

    class Meta:
        db_table = "books"

    user = models.ForeignKey(
        User,
        related_name = 'books',
        on_delete = models.SET_NULL,
        null = True
    )

    title = models.CharField(
        verbose_name = "title",
        max_length = 1000,
        null = True
    )

    thumb_path = models.CharField(
        verbose_name = "thumb_path",
        max_length = 1000,
        null = True
    )

    is_public = models.BooleanField(
        verbose_name = "public or not",
        default = False
    )

    senkei_sente = models.CharField(
        verbose_name = "senkei sente",
        max_length = 1000,
        null = True
    )

    senkei_gote = models.CharField(
        verbose_name = "senkei gote",
        max_length = 1000,
        null = True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    