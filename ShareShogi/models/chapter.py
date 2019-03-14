from django.db import models

# db
from accounts.models.user import User
from ShareShogi.models.book import Book

class Chapter(models.Model):

    class Meta:
        db_table = "chapters"

    book = models.ForeignKey(
        Book,
        related_name = 'chapters',
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    