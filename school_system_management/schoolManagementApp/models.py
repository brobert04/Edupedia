from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class SessionYears(models.Model):
    id = models.AutoField(primary_key=True)
    startYear = models.DateField()
    endYear = models.DateField()
    object = models.Manager()
    
class UserCustom(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(default=1, max_length=30, choices=user_type_data)


# MODELUL PENTRU ADMIN(IN CAZUL ACESTA, DIRECTORUL SCOLII)
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(UserCustom, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# MODELUL PENTRU STAFF/PROFESORI
class Staff(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(UserCustom, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    address = models.TextField(max_length=500)


# MODEL PENTRU CURS/URI 
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)


# MODEL PENTRU MATERIE
class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    staffId = models.ForeignKey(UserCustom, on_delete=models.CASCADE)


# MODELUL PENTRU STUDENT
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(UserCustom, on_delete=models.CASCADE)
    address = models.TextField(max_length=300)
    profile_picture = models.FileField()
    gender = models.CharField(max_length=300)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    session_id = models.ForeignKey(SessionYears, on_delete=models.CASCADE)



# MODELUL PENTRU INREGISTRAREA PREZENTEI
class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=False)
    subjectID = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session_id = models.ForeignKey(SessionYears, on_delete=models.CASCADE)


# MODELUL PENTRU RAPORTUL PREZENTEI LA CURSURI
class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendanceID = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


# MODELUL PENTRU INREGISTRAREA ELEVILOR CARE PARASESC SCOALA/PLATFORMA
class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    leaveDate = models.CharField(max_length=300)


# MODELUL PENTRU INREGISTRAREA PROFESORILOR CARE PARASESC SCOALA   
class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staffID = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    leaveDate = models.CharField(max_length=300)


# MODEL PENTRU INREGISTRAREA FEEDBACK-ULUI ELEVULUI
class FeedbackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedbackReply = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)


# MODEL PENTRU INREGISTRAREA FEEDBACK-ULUI PROFESORULUI
class FeedbackStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staffID = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedbackReply = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)


# MODEL PENTRU NOTIFICARILE PRIMITE DE ELEVI/STUDENTI
class StudentNotification(models.Model):
    id = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)


# MODEL PENTRU NOTIFICARILE PRIMITE DE PROFESORI
class StaffNotification(models.Model):
    id = models.AutoField(primary_key=True)
    staffID = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)


# ATUNCI CAND UN NOU USER ESTE CREAT, SE VA ADAUGA AUTOMAT IN NOU RAND FIE IN MODELUL DIRECTORULUI, INVATATORULUI SAU STUDENTULUI
@receiver(post_save, sender=UserCustom)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance, courseId=Course.objects.get(id=1),session_id=SessionYears.object.get(id=1), address="",profile_picture="",gender="")


# ACEASTA METODA VA FI EXECUTATA PENTRU A SALVA INFORMATIILE DUPA CE EXECUTIA FUNCTIEI DE MAI SUS SE VA FI TERMINAT
@receiver(post_save, sender=UserCustom)
def save_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
