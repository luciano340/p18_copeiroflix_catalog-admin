# Generated by Django 5.1 on 2024-09-08 12:08

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CastMemberModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_date', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'db_table': 'cast_member',
            },
        ),
    ]
