# Generated by Django 5.0.6 on 2024-07-28 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_reservation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]