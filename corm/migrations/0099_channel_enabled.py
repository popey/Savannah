# Generated by Django 3.0.4 on 2021-01-22 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0098_auto_20210122_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
