# Generated by Django 5.0.6 on 2024-07-25 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artwork', '0006_alter_artwork_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistinquiry',
            name='art_work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='artwork.artwork'),
        ),
    ]