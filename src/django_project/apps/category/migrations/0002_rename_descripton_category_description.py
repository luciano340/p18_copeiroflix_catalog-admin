# Generated by Django 5.1 on 2024-08-24 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='descripton',
            new_name='description',
        ),
    ]
