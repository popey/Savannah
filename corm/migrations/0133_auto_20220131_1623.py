# Generated by Django 3.1.2 on 2022-01-31 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0132_auto_20220126_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='inactivity_threshold_days',
            field=models.PositiveSmallIntegerField(default=30, help_text='Number of days of inactivity before triggering a notification'),
        ),
        migrations.AddField(
            model_name='community',
            name='inactivity_threshold_previous_activity',
            field=models.PositiveSmallIntegerField(default=50, help_text='Amount of previous activity required before you will be notified that a member has become inactive.'),
        ),
        migrations.AddField(
            model_name='community',
            name='inactivity_threshold_previous_days',
            field=models.PositiveSmallIntegerField(default=90, help_text='Number of days into the past to check for activity to meet the notification threshold'),
        ),
        migrations.AddField(
            model_name='community',
            name='resuming_threshold_days',
            field=models.PositiveSmallIntegerField(default=30, help_text='Number of days of inactivity before triggering a notification on new activity'),
        ),
        migrations.AddField(
            model_name='community',
            name='resuming_threshold_previous_activity',
            field=models.PositiveSmallIntegerField(default=20, help_text='Amount of previous activity required before you will be notified that an inactive member had become active again'),
        ),
        migrations.AddField(
            model_name='community',
            name='resuming_threshold_previous_days',
            field=models.PositiveSmallIntegerField(default=90, help_text='Number of days into the past to check for activity to meet the notification threshold'),
        ),
    ]
