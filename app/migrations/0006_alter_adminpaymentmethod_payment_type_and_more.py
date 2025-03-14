# Generated by Django 5.1.4 on 2025-01-25 14:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_plans_plan_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminpaymentmethod',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('WALLET', 'WALLET'), ('BTC', 'BTC'), ('ETH', 'ETH'), ('CASH APP', 'CASH APP'), ('PAYPAL', 'PAYPAL')], max_length=400),
        ),
        migrations.CreateModel(
            name='CustomerPaymentInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(blank=True, choices=[('WALLET', 'WALLET'), ('BTC', 'BTC'), ('ETH', 'ETH'), ('CASH APP', 'CASH APP'), ('PAYPAL', 'PAYPAL')], max_length=400)),
                ('payment_address', models.CharField(blank=True, max_length=400)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
