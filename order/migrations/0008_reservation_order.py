# Generated by Django 5.0.6 on 2024-08-09 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_alter_refundimg_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='order',
            field=models.ForeignKey(default=139, on_delete=django.db.models.deletion.CASCADE, to='order.orderitem'),
            preserve_default=False,
        ),
    ]