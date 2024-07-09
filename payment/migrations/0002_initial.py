# Generated by Django 5.0.6 on 2024-07-08 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0002_initial'),
        ('payment', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payment.paymentstatus'),
        ),
        migrations.AddField(
            model_name='settlement',
            name='order_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.orderitem'),
        ),
        migrations.AddField(
            model_name='settlement',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.seller'),
        ),
        migrations.AddField(
            model_name='settlement',
            name='settlement_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payment.settlementstatus'),
        ),
    ]
