import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from schoolManagementApp.models import Attendance, AttendanceReport, Course, FeedbackStudent, LeaveReportStudent, Student, Subject, UserCustom,StudentNotification, StudentResults
from datetime import datetime


# ACEASTA FUNCTIE RANDEAZA PAGINA DE HOME A STUDENTULUI SI AJUTA LA INCARCAREA DINAMICA A CHARTURILOR RESPECTIVE
def student_home(request):
    student = Student.objects.get(admin=request.user.id)
    leave_report = LeaveReportStudent.objects.filter(studentID=student).count
    
    try:
        percentage_present = AttendanceReport.objects.filter(studentID=student, status=True).count() / AttendanceReport.objects.filter(studentID=student, status=False).count()
    except:
         percentage_present = AttendanceReport.objects.filter(studentID=student, status=True).count() / 1
    
    present_total = AttendanceReport.objects.filter(studentID=student, status=True).count()
    absent = AttendanceReport.objects.filter(studentID=student, status=False).count()
    course = Course.objects.get(id=student.courseId.id)
    subjects = Subject.objects.filter(courseId=course).count()
    
    subject_name=[]
    subject_present=[]
    subject_absent=[]
    subjectData = Subject.objects.filter(courseId=student.courseId)
    for subject in subjectData:
        attendance = Attendance.objects.filter(subjectID=subject.id)
        att_present = AttendanceReport.objects.filter(attendanceID__in=attendance, status=True, studentID=student.id).count()
        att_absent = AttendanceReport.objects.filter(attendanceID__in=attendance, status=False, studentID=student.id).count()
        subject_name.append(subject.name)
        subject_present.append(att_present)
        subject_absent.append(att_absent)

    notifications = StudentNotification.objects.filter(studentID=student.id)
    notf_number  = notifications.count()
    return render(request, 'student_templates/home.html', {"leave_report":leave_report, "present":percentage_present, "absent":absent, "subjects":subjects, "course":course, "total_present":present_total, "subject_name":subject_name, "subject_present":subject_present, "subject_absent":subject_absent, "notifications":notifications, "notf_number":notf_number})

# ACEASTA FUNCTIE RANDEAZA PAGINA DE VIZUALIZARE A PROPRIILOR ABSENTE
def student_view_attendance(request):
    student = Student.objects.get(admin=request.user.id)
    course = Course.objects.get(id=student.courseId.id)
    subjects = Subject.objects.filter(courseId=course)
    return render(request, 'student_templates/view_own_attendance.html', {"subjects":subjects})

# ACEASTA FUNCTIE AJUTA LA PRINTAREA ABSENTELOR INTR O PAGINA SEPARATA
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

# ACEASTA FUNCTIE RANDEAZA PAGINA DE TRIMITERE A FEEDBACK ULUI
def student_send_feedback(request):
    student = Student.objects.get(admin=request.user.id)
    feedback = FeedbackStudent.objects.filter(studentID=student)
    return render(request, "student_templates/student_send_feedback.html", {"feedback": feedback})

# ACEASTA FUNCTIE SALVEAZA FEEDBACK UL TRIMIS IN BAZA DE DATE
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
        try:
            user = UserCustom.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, 'Profile information have been updated!')
            return HttpResponseRedirect(reverse('student_profile'))
        except:
            messages.error(request,'The platform could not process the request. Try again!')
            return HttpResponseRedirect(reverse('student_profile'))


def student_contact_information(request):
    principal = UserCustom.objects.filter(user_type=1)
    staff = UserCustom.objects.filter(user_type=2)
    return render(request, "student_templates/contact-information.html",{"principal":principal, "staff":staff}  )


def delete_notification_student(request, notification_id):
    notification = StudentNotification.objects.get(id=notification_id)
    notification.delete()
    return HttpResponseRedirect(reverse('student_dashboard'))


def delete_all_notifications_student(request):
    student = Student.objects.get(admin=request.user.id)
    notifications = StudentNotification.objects.filter(studentID=student)
    notifications.delete()
    return HttpResponseRedirect(reverse('student_dashboard'))


def view_results(request):
    student = Student.objects.get(admin=request.user.id)
    student_results = StudentResults.objects.filter(studentID=student.id)
    return render(request, "student_templates/view_results.html", {"student_results": student_results})