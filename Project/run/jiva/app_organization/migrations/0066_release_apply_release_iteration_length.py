# Generated by Django 5.0.3 on 2024-11-25 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0065_release_release_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='apply_release_iteration_length',
            field=models.PositiveIntegerField(default=2),
        ),
    ]
