# Generated by Django 5.1 on 2024-09-28 16:55

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cast_member', '0001_initial'),
        ('category', '0005_remove_category_createed_date_category_created_date_and_more'),
        ('genre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioVideoMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('checksum', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('raw_location', models.CharField(max_length=1024)),
                ('encoded_location', models.CharField(max_length=1024)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('PROCESSING', 'PROCESSING'), ('COMPLETED', 'COMPLETED'), ('ERROR', 'ERROR')], max_length=20)),
            ],
            options={
                'db_table': 'videos_audiovideomedia',
            },
        ),
        migrations.CreateModel(
            name='ImageMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('checksum', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('raw_location', models.CharField(max_length=1024)),
            ],
            options={
                'db_table': 'videos_imagemedia',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('launch_at', models.DateField()),
                ('duration', models.DecimalField(decimal_places=2, max_digits=10)),
                ('published', models.BooleanField()),
                ('rating', models.CharField(choices=[('ER', 'ER'), ('L', 'L'), ('AGE_10', 'AGE_10'), ('AGE_12', 'AGE_12'), ('AGE_14', 'AGE_14'), ('AGE_16', 'AGE_16'), ('AGE_18', 'AGE_18')], max_length=10)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_date', models.DateTimeField(default=None, null=True)),
                ('cast_member', models.ManyToManyField(related_name='videos', to='cast_member.castmembermodel')),
                ('categories', models.ManyToManyField(related_name='videos', to='category.category')),
                ('genres', models.ManyToManyField(related_name='videos', to='genre.genre')),
            ],
            options={
                'db_table': 'videos',
            },
        ),
    ]
