# Generated by Django 5.0.3 on 2024-11-03 07:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0027_projectadministration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
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
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_project_templates', to=settings.AUTH_USER_MODEL)),
                ('org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='org_project_templates', to='app_organization.organization')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
    ]
