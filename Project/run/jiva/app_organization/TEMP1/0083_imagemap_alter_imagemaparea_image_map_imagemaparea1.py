# Generated by Django 5.0.3 on 2024-11-26 18:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0082_remove_oldimagemaparea_image_map_delete_imagemap_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
                ('blocked_count', models.PositiveIntegerField(default=0)),
                ('done', models.BooleanField(default=False)),
                ('done_at', models.DateTimeField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('image', models.FileField(blank=True, null=True, upload_to='folder_image_maps/')),
                ('original_width', models.PositiveIntegerField(blank=True, null=True)),
                ('original_height', models.PositiveIntegerField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_image_maps', to=settings.AUTH_USER_MODEL)),
                ('pro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pro_image_maps', to='app_organization.project')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='imagemaparea',
            name='image_map',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='app_organization.imagemap'),
        ),
        migrations.CreateModel(
            name='ImageMapArea1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
                ('blocked_count', models.PositiveIntegerField(default=0)),
                ('done', models.BooleanField(default=False)),
                ('done_at', models.DateTimeField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('shape', models.CharField(blank=True, choices=[('rect', 'Rectangle'), ('circle', 'Circle'), ('poly', 'Polygon')], max_length=20, null=True)),
                ('coords', models.TextField(blank=True, help_text='Comma-separated coordinates (e.g., x1,y1,x2,y2)', null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('hover_text', models.CharField(blank=True, max_length=255, null=True)),
                ('image_map', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='app_organization.orgimagemap')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
    ]
