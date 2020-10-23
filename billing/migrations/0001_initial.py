# Generated by Django 3.0.4 on 2020-08-31 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('corm', '0085_community_status'),
        ('djstripe', '0006_2_3'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Management',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corm.Community')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.Company')),
                ('subscription', models.ForeignKey(blank=True, help_text="The team's Stripe Subscription object, if it exists", null=True, on_delete=django.db.models.deletion.SET_NULL, to='djstripe.Subscription')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='communities',
            field=models.ManyToManyField(through='billing.Management', to='corm.Community'),
        ),
        migrations.AddField(
            model_name='company',
            name='customer',
            field=models.ForeignKey(blank=True, help_text="The team's Stripe Subscription object, if it exists", null=True, on_delete=django.db.models.deletion.SET_NULL, to='djstripe.Customer'),
        ),
    ]
