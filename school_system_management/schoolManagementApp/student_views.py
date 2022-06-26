import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from schoolManagementApp.models import Attendance, AttendanceReport, Course, FeedbackStudent, LeaveReportStudent, Student, Subject, UserCustom


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

def student_send_feedback(request):
    student = Student.objects.get(admin=request.user.id)
    feedback = FeedbackStudent.objects.filter(studentID=student)
    return render(request, "student_templates/student_send_feedback.html", {"feedback": feedback})

def student_feedback(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        feedback_msg = request.POST.get("feedbackMessage")
        student = Student.objects.get(admin = request.user.id)
        
        try:
            feedback = FeedbackStudent(studentID=student, feedback=feedback_msg, feedbackReply="")
            feedback.save()
            messages.success(request, 'Your feedback has been sent!' )
            return HttpResponseRedirect(reverse("student_send_feedback"))
        except:
            messages.error(request, 'The platform could not process the request. Try again!')
            return HttpResponseRedirect(reverse("student_send_feedback"))


def student_applyfor_leave(request):
    student = Student.objects.get(admin=request.user.id)
    data  = LeaveReportStudent.objects.filter(studentID=student)
    return render(request, "student_templates/student_leave_application.html", {"leaveData": data})


def student_send_leave(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        leave_date = request.POST.get("leave_date") 
        leave_reason = request.POST.get("leave_reason")
        
        student = Student.objects.get(admin=request.user.id)
        
        try:
            report = LeaveReportStudent(leaveDate=leave_date, studentID=student,leaveMessage=leave_reason, status=0)
            report.save()
            messages.success(request, 'Your leave application has been sent and it will be reviewed by the principal!' )
            return HttpResponseRedirect('/student_applyfor_leave')
        except:
             messages.error(request, 'The platform could not process the request. Try again!')
             return HttpResponseRedirect('/student_applyfor_leave')
         
         

def student_profile(request):
    user = UserCustom.objects.get(id=request.user.id)
    student = Student.objects.get(admin=user)
    return render(request, "student_templates/student_profile.html", {"user":user, "student":student})


def student_profile_save(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        address = request.POST.get("address")
        try:
            user = UserCustom.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            student = Student.objects.get(admin=user)
            student.address = address
            student.save()
            messages.success(request, 'Profile information have been updated!')
            return HttpResponseRedirect(reverse('student_profile'))
        except:
            messages.error(request,'The platform could not process the request. Try again!')
            return HttpResponseRedirect(reverse('student_profile'))