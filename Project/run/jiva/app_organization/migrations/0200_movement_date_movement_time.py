# Generated by Django 5.1.5 on 2025-03-07 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0199_remove_movement_from_state_remove_movement_to_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movement',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
