# Generated by Django 3.1.2 on 2022-09-19 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0146_uploadedfile_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='import_tag',
            field=models.ForeignKey(blank=True, help_text='Tag all Members in this file', null=True, on_delete=django.db.models.deletion.SET_NULL, to='corm.tag'),
        ),
    ]
