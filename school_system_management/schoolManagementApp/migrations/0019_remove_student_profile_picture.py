# Generated by Django 4.0.6 on 2022-11-05 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolManagementApp', '0018_alter_student_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='profile_picture',
        ),
    ]
