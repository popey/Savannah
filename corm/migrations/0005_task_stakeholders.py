# Generated by Django 3.0.4 on 2020-03-05 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0004_auto_20200305_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='stakeholders',
            field=models.ManyToManyField(to='corm.Member'),
        ),
    ]
