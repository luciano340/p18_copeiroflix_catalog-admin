from datetime import datetime
from uuid import uuid4
from django.db import models


class Genre(models.Model):
    app_label = "genre"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField('category.Category', related_name='genres')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=datetime.now)
    updated_date = models.DateTimeField(default=None, null=True)

    class Meta:
        db_table = 'genres'