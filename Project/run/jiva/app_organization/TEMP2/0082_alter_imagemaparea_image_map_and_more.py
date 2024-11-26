# Generated by Django 5.0.3 on 2024-11-26 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0081_orgimagemap_imagemaparea1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemaparea',
            name='image_map',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='app_organization.orgimagemap'),
        ),
        migrations.RemoveField(
            model_name='imagemaparea1',
            name='image_map',
        ),
        migrations.DeleteModel(
            name='ImageMap',
        ),
        migrations.DeleteModel(
            name='ImageMapArea1',
        ),
    ]
