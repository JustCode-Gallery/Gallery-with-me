# Generated by Django 5.0.6 on 2024-07-30 09:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibit', '0006_alter_artexhibitposter_poster_url'),
        ('user', '0005_remove_department_university_university_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artexhibit',
            name='department',
        ),
        migrations.AddField(
            model_name='artexhibit',
            name='university_department',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.PROTECT, related_name='exhibit_departments', to='user.university_department'),
            preserve_default=False,
        ),
    ]