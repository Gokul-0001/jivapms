# Generated by Django 5.0.3 on 2024-12-14 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0117_project_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='backlog',
            name='flat_backlog_type',
            field=models.CharField(choices=[('USER STORY', 'User Story'), ('TASK', 'Task'), ('BUG', 'Bug'), ('ENHANCEMENT', 'Enhancement'), ('DEFECT', 'Defect'), ('ISSUE', 'Issue'), ('REFACTOR', 'Refactor'), ('TECH_DEBT', 'Tech Debt'), ('TEST', 'Test'), ('DOC', 'Doc'), ('SPIKE', 'Spike')], default='USER STORY', max_length=100),
        ),
        migrations.AddField(
            model_name='backlog',
            name='size',
            field=models.CharField(choices=[('0', '0'), ('0.5', '0.5'), ('1', '1'), ('2', '2'), ('3', '3'), ('5', '5'), ('8', '8'), ('13', '13'), ('20', '2'), ('100', '100'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')], default='0', max_length=100),
        ),
        migrations.AddField(
            model_name='backlog',
            name='status',
            field=models.CharField(choices=[('Backlog', 'Backlog'), ('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done'), ('Blocked', 'Blocked'), ('Unblocked', 'Unblocked'), ('Deleted', 'Deleted'), ('Archived', 'Archived')], default='Backlog', max_length=100),
        ),
    ]
