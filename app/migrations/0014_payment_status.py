# Generated by Django 5.1.4 on 2025-03-09 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_customuser_program_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Success', 'Success')], default='Pending', max_length=400),
        ),
    ]
