# Generated by Django 3.2.9 on 2021-11-23 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KidsStepShop', '0002_auto_20211123_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
    ]
