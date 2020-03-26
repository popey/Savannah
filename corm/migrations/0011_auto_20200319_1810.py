# Generated by Django 3.0.4 on 2020-03-19 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0010_auto_20200319_1804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='channel',
        ),
        migrations.AlterField(
            model_name='contact',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corm.Source'),
        ),
    ]
