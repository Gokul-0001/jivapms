# Generated by Django 5.0.3 on 2024-12-14 17:23

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0119_backlog_owner_subtasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='backlog',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Normal', 'Normal'), ('Medium', 'Medium'), ('High', 'High'), ('Critical', 'Critical')], default='Normal', max_length=10),
        ),
        migrations.AlterField(
            model_name='backlog',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Project', to='app_organization.backlog'),
        ),
        migrations.AlterField(
            model_name='backlog',
            name='type',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='backlog_types', to='app_organization.backlogtype'),
        ),
    ]
