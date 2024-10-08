# Generated by Django 5.1 on 2024-08-24 19:43

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('descripton', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('createed_date', models.DateField(default=datetime.datetime.now)),
                ('updated_date', models.DateField()),
            ],
            options={
                'db_table': 'categories',
            },
        ),
    ]
