# Generated by Django 5.0.6 on 2024-07-25 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_orderitem_address_reservation_cancel_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
