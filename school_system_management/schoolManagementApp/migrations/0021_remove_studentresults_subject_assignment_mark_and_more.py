# Generated by Django 4.0.6 on 2022-11-06 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolManagementApp', '0020_remove_studentresults_subject_exam_mark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentresults',
            name='subject_assignment_mark',
        ),
        migrations.AddField(
            model_name='studentresults',
            name='subject_exam_mark',
            field=models.FloatField(default=0),
        ),
    ]
