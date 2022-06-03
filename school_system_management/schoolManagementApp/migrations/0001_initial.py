# Generated by Django 4.0.4 on 2022-06-02 20:10

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCustom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(1, 'Admin'), (2, 'Staff'), (3, 'Student')], default=1, max_length=30)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('modifiedAt', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('modifiedAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('modifiedAt', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField(max_length=500)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.TextField(max_length=300)),
                ('profile_picture', models.FileField(upload_to='')),
                ('gender', models.CharField(max_length=300)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('modifiedAt', models.DateTimeField(auto_now_add=True)),
                ('startYear', models.DateField()),
                ('finishYear', models.DateField()),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('courseId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.course')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('modifiedAt', models.DateTimeField(auto_now_add=True)),
                ('courseId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.course')),
                ('staffId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.staff')),
            ],
        ),
        migrations.CreateModel(
            name='StudentNotification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('studentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.student')),
            ],
        ),
        migrations.CreateModel(
            name='StaffNotification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('staffID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.staff')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('leaveDate', models.CharField(max_length=300)),
                ('studentID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.student')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('leaveDate', models.CharField(max_length=300)),
                ('staffID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.staff')),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedbackReply', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('studentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.student')),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.CharField(max_length=255)),
                ('feedbackReply', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('staffID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.staff')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('attendanceID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.attendance')),
                ('studentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.student')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='subjectID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolManagementApp.subject'),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('modifiedAt', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
