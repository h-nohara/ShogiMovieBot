
from django.db import models
from accounts.models.user import User
from accounts.models.project import Project

# model
from accounts.models.user import User


class Info(models.Model):

    class Meta:
        db_table = "infos"

    user = models.ForeignKey(
        User,
        related_name = 'infos',
        on_delete = models.SET_NULL,
        null = True
    )

    message = models.CharField(
        verbose_name = "message",
        max_length = 1000,
        null = True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    