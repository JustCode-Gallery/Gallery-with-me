# Generated by Django 5.0.6 on 2024-07-23 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibit', '0005_alter_artexhibit_latitude_alter_artexhibit_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artexhibitposter',
            name='poster_url',
            field=models.ImageField(upload_to='poster_image/'),
        ),
    ]
