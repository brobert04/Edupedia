# Generated by Django 4.0.4 on 2022-06-18 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolManagementApp', '0002_alter_sessionyears_managers_alter_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
