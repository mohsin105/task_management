# Generated by Django 5.1.6 on 2025-02-15 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_task_assigned_to'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
