# Generated by Django 5.0.3 on 2024-11-15 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0038_opsvaluestreamstep'),
    ]

    operations = [
        migrations.AddField(
            model_name='devvaluestreamstep',
            name='delay',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='devvaluestreamstep',
            name='value',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
