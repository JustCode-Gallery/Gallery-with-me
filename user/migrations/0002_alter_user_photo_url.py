# Generated by Django 5.0.6 on 2024-07-09 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo_url',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
