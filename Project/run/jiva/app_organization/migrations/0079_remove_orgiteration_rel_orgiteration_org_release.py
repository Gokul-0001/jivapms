# Generated by Django 5.0.3 on 2024-11-26 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0078_delete_orgiterationx'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orgiteration',
            name='rel',
        ),
        migrations.AddField(
            model_name='orgiteration',
            name='org_release',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='org_release_org_iterations', to='app_organization.orgrelease'),
        ),
    ]
