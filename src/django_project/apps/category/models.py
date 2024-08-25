from datetime import datetime
from django.db import models
import uuid


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=datetime.now)
    updated_date = models.DateTimeField(default=None, null=True)

    class Meta:
        db_table = "categories"
    
    def __str__(self):
        return self.name