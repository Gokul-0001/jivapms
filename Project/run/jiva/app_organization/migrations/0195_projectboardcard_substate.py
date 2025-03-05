# Generated by Django 5.1.5 on 2025-03-04 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0194_projectboardstate_apply_wip_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectboardcard',
            name='substate',
            field=models.CharField(choices=[('Doing', 'Doing'), ('Done', 'Done')], default='Doing', max_length=10),
        ),
    ]
