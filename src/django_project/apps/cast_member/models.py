from datetime import datetime
from django.db import models
import uuid


class CastMemberModel(models.Model):
    app_label = "cast_member"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=datetime.now)
    updated_date = models.DateTimeField(default=None, null=True)

    class Meta:
        db_table = "cast_member"
    
    def __str__(self):
        return self.name