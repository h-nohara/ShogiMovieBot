from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    line_id = models.CharField(
        verbose_name = "line_id",
        max_length = 1000,
        null = True
    )

    line_display_name = models.CharField(
        verbose_name = "line_display_name",
        max_length = 1000,
        null = True
    )

    line_thumb_path = models.CharField(
        verbose_name = "line_thumb_path",
        max_length = 1000,
        null = True
    )

