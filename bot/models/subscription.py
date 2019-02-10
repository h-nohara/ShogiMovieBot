
from django.db import models
from accounts.models.user import User
from accounts.models.project import Project

# model
from accounts.models.user import User
from bot.models.scenario import Scenario


class Subscription(models.Model):

    class Meta:
        db_table = "subscriptions"

    reader = models.ForeignKey(
        User,
        related_name = 'subscriptions',
        on_delete = models.SET_NULL,
        null = True
    )

    author = models.ForeignKey(
        User,
        related_name = 'author',
        on_delete = models.SET_NULL,
        null = True
    )

    scenario = models.ForeignKey(
        Scenario,
        related_name = 'subscriptions',
        on_delete = models.SET_NULL,
        null = True
    )

    is_scenario_public = models.BooleanField(
        verbose_name = "scenario public or not",
        default = False
    )

    is_enabled = models.BooleanField(
        verbose_name = "enabled",
        default = False
    )

    # "random",
    kind = models.CharField(
        verbose_name = "kind",
        max_length = 1000,
        null = True,
        default = "random"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    