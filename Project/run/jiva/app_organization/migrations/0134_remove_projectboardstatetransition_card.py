# Generated by Django 5.0.3 on 2024-12-16 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0133_delete_projectboardcolumn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectboardstatetransition',
            name='card',
        ),
    ]
