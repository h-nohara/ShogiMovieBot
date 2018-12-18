from django.db import models


class KifuMovie(models.Model):

    class Meta:
        db_table = "kifu_movies"


    path = models.CharField(
        verbose_name = "path",
        max_length = 1000,
        null = True
    )

    # 戦型
    opening = models.CharField(
        verbose_name = "opening",
        max_length = 1000,
        null = True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    