# Generated by Django 5.1.4 on 2025-03-09 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_customerpaymentinformation_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerpaymentinformation',
            options={'verbose_name': 'Customer Payment Information', 'verbose_name_plural': 'Customer Payment Information'},
        ),
        migrations.RemoveField(
            model_name='payment',
            name='is_tax',
        ),
        migrations.AddField(
            model_name='payment',
            name='wallet',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AddField(
            model_name='payment',
            name='wallet_address',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='payment',
            name='transaction_type',
            field=models.CharField(blank=True, choices=[('FUNDING', 'FUNDING'), ('WITHDRAWAL', 'WITHDRAWAL')], max_length=400),
        ),
    ]
