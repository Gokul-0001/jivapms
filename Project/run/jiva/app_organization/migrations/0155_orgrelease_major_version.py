# Generated by Django 5.0.3 on 2024-12-25 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0154_orgrelease_release_official_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgrelease',
            name='major_version',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
