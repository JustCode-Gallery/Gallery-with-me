# Generated by Django 5.0.6 on 2024-07-12 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artwork', '0003_artwork_is_reservable_alter_artimage_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artimage',
            name='image_url',
            field=models.ImageField(upload_to='artwork_image/'),
        ),
    ]
