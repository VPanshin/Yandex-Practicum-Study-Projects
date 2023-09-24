from django.db import models


class CreatedModel(models.Model):
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    text = models.TextField(
        'Текст комментария',
    )

    class Meta:
        abstract = True
