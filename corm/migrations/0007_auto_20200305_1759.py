# Generated by Django 3.0.4 on 2020-03-05 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0006_auto_20200305_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='done',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
