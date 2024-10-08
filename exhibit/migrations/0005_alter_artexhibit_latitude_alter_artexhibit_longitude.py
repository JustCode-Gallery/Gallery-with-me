# Generated by Django 5.0.6 on 2024-07-15 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibit', '0004_artexhibit_latitude_artexhibit_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artexhibit',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=25, null=True),
        ),
        migrations.AlterField(
            model_name='artexhibit',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=25, null=True),
        ),
    ]
