from django.db import models

# db
from accounts.models.user import User
from ShareShogi.models.book import Book
from ShareShogi.models.chapter import Chapter

class Scene(models.Model):

    class Meta:
        db_table = "scenes"

    chapter = models.ForeignKey(
        Chapter,
        related_name = 'scenes',
        on_delete = models.SET_NULL,
        null = True
    )

    text = models.CharField(
        verbose_name = "text",
        max_length = 1000,
        null = True
    )

    image_url = models.CharField(
        verbose_name = "image_url",
        max_length = 1000,
        null = True
    )

    movie_url = models.CharField(
        verbose_name = "movie_url",
        max_length = 1000,
        null = True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    