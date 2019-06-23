from django.db import models

# db
from accounts.models.user import User

class NextItte(models.Model):

    class Meta:
        db_table = "nextIttes"

    user = models.ForeignKey(
        User,
        related_name = 'nextIttes',
        on_delete = models.SET_NULL,
        null = True
    )

    title = models.CharField(
        verbose_name = "title",
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

    choice_right = models.CharField(
        verbose_name = "title",
        max_length = 1000,
        null = True
    )

    choice_false_1 = models.CharField(
        verbose_name = "choice_false_1",
        max_length = 1000,
        null = True
    )

    choice_false_2 = models.CharField(
        verbose_name = "choice_false_2",
        max_length = 1000,
        null = True
    )

    message_question = models.CharField(
        verbose_name = "message_question",
        max_length = 1000,
        null = True
    )

    message_answer = models.CharField(
        verbose_name = "message_answer",
        max_length = 1000,
        null = True
    )


    is_public = models.BooleanField(
        verbose_name = "public or not",
        default = False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    