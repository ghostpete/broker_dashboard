# Generated by Django 5.1.4 on 2025-03-09 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_adminwallet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='wallet_address',
        ),
    ]
