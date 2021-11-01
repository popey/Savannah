# Generated by Django 3.1.2 on 2021-10-29 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0130_source_api_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventattendee',
            name='role',
            field=models.CharField(choices=[('guest', 'Guest'), ('host', 'Host'), ('speaker', 'Speaker')], default='guest', max_length=32),
        ),
        migrations.AlterField(
            model_name='companydomains',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='corm.company'),
        ),
        migrations.AlterField(
            model_name='project',
            name='member_tag',
            field=models.ForeignKey(blank=True, help_text="Any activity by a member with this tag will be included in this project's activity", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects_by_member', to='corm.tag', verbose_name='Member tag'),
        ),
        migrations.AlterField(
            model_name='project',
            name='tag',
            field=models.ForeignKey(blank=True, help_text="Any content with this tag will be included in this project's activity", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects_by_content', to='corm.tag', verbose_name='Content tag'),
        ),
        migrations.AlterField(
            model_name='source',
            name='api_key',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
