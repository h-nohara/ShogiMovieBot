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

    line_display_name = models.CharField(
        verbose_name = "line_display_name",
        max_length = 1000,
        null = True
    )

    nickname = models.CharField(
        verbose_name = "nickname",
        max_length = 1000,
        null = True,
        default = "匿名さん"
    )


    # 配信配信

    # ランダム購読

    is_enabled_RandomSubscription_own_scenario = models.BooleanField(
        verbose_name = "enabled_RandomSubscription_own_scenario",
        default = True
    )

    is_enabled_RandomSubscription_others_scenario = models.BooleanField(
        verbose_name = "enabled_RandomSubscription_ohters_scenario",
        default = False
    )

    interval_RandomSubscription = models.IntegerField(
        verbose_name = "interval_random_distribution",
        default = 1
    )

    next_date_RandomSubscription = models.DateTimeField(auto_now_add=False, null=True)

