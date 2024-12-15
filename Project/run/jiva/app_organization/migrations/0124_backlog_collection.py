# Generated by Django 5.0.3 on 2024-12-15 12:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0123_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='backlog',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='backlog_collections', to='app_organization.collection'),
        ),
    ]
