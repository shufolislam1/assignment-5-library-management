# Generated by Django 4.2.7 on 2024-03-03 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction_and_borrow', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]