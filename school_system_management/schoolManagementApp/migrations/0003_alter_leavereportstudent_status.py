# Generated by Django 4.0.4 on 2022-06-26 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolManagementApp', '0002_alter_feedbackstaff_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportstudent',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
