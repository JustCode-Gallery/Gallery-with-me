# Generated by Django 5.0.6 on 2024-07-30 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_orderitem_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refundimg',
            name='image_url',
            field=models.ImageField(upload_to='refund_images/'),
        ),
    ]