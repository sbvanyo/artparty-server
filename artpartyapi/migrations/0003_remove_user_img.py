# Generated by Django 4.1.3 on 2024-03-13 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artpartyapi', '0002_artwork_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='img',
        ),
    ]
