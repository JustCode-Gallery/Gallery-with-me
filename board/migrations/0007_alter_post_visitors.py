# Generated by Django 5.0.6 on 2024-07-18 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_post_visitors_alter_post_exhibit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visitors',
            field=models.IntegerField(default=0),
        ),
    ]