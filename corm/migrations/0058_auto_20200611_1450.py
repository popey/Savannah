# Generated by Django 3.0.4 on 2020-06-11 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0057_community_logo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='community',
            options={'ordering': ('name',), 'verbose_name': 'Community', 'verbose_name_plural': 'Communities'},
        ),
        migrations.RemoveField(
            model_name='community',
            name='icon_path',
        ),
    ]
