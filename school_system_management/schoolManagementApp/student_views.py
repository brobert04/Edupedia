import datetime
from django.http import HttpResponse
from django.shortcuts import render

from schoolManagementApp.models import Attendance, AttendanceReport, Course, Student, Subject, UserCustom


def student_home(request):
    return render(request, 'student_templates/home.html')

def student_view_attendance(request):
    student = Student.objects.get(admin=request.user.id)
    course = Course.objects.get(id=student.courseId.id)
    subjects = Subject.objects.filter(courseId=course)
    return render(request, 'student_templates/view_own_attendance.html', {"subjects":subjects})

def student_view_attendance_data(request):
    subject = request.POST.get("subject")
    startDate = request.POST.get("startDate")
    endDate = request.POST.get("endDate")
    
    start_date_transform = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    end_date_transform = datetime.datetime.strptime(endDate,"%Y-%m-%d").date()
    
    subject_object = Subject.objects.get(id=subject)
    user  = UserCustom.objects.get(id=request.user.id)
    student = Student.objects.get(admin=user)
    
    attendance = Attendance.objects.filter(date__range=(start_date_transform, end_date_transform), subjectID=subject_object)
    
    attendance_report = AttendanceReport.objects.filter(attendanceID__in=attendance, studentID=student)

    return render(request, "student_templates/own_attendance_data.html", {"report": attendance_report, "subject": subject_object})