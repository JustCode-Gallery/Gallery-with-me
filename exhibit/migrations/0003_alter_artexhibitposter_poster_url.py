# Generated by Django 5.0.6 on 2024-07-09 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibit', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artexhibitposter',
            name='poster_url',
            field=models.ImageField(upload_to=''),
        ),
    ]
