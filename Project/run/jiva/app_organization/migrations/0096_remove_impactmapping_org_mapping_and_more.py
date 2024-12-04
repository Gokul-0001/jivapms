# Generated by Django 5.0.3 on 2024-12-04 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0095_remove_impactmapping_orgmapping_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impactmapping',
            name='org_mapping',
        ),
        migrations.AddField(
            model_name='impactmapping',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_impact_mappings', to='app_organization.organization'),
        ),
    ]
