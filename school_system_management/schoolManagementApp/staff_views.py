import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from requests import session
from schoolManagementApp.models import Attendance, AttendanceReport, FeedbackStaff, LeaveReportStaff, SessionYears, Staff, Student, Subject, UserCustom
from  django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# FUNCTIA PENTRU A RANDA PAGINA DE DASHBOARD A MEMBRULUI STAFF-ULUI
def staff_home(request):
    return render(request, 'staff_templates/home.html')

# FUNCTIA PENTRU A RANDA PAGINA DE STABILIRE A PREZENTEI LA CURS
def student_attendance(request):
    subjects = Subject.objects.filter(staffId = request.user.id)
    session = SessionYears.object.all()
    return render(request, 'staff_templates/student_attendance.html', {"subjects": subjects, "session":session})


# FOLOSIM AJAX PENTRU A DETERMINA ELEVII PREZENTI LA MATERIA RESPECTIVA SI PREZENTI IN ACEA SESIUNE
@csrf_exempt
def get_students(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    
    subject = Subject.objects.get(id=subject_id)
    session = SessionYears.object.get(id=session_id)
    student = Student.objects.filter(courseId=subject.courseId, session_id=session)
    data = []
    for s in student:
        d = {"id": s.admin.id, "name": f"{s.admin.first_name} {s.admin.last_name}"}
        data.append(d) 
    return JsonResponse(json.dumps(data),content_type="application/json", safe=False)


# PRELUAM DATELE REFERIOTOARE LA PREZENTA DIN DIV-UL RANDAT DINAMIC DIN PARGINA 'STUDENT_ATTENDANCE.HTML' SI LE SALVAM IN MODELUL DE PREZENTA 'ATTENDANCE'. ULTERIOR, PE BAZA ACESTOR INFORMATII, CREEZ SI RAPORTUL DE PREZENTA
@csrf_exempt
def attendance_data(request):
    students_id = request.POST.get("students_id")
    attendance_date = request.POST.get("attendanceDate")
    subject_id = request.POST.get("subject_id")
    session_id = request.POST.get("session_id")
     
    sub_mod = Subject.objects.get(id=subject_id)
    sess_mod  = SessionYears.object.get(id=session_id)
    new_student_data = json.loads(students_id)
    try:
        attendance  = Attendance(subjectID=sub_mod, session_id=sess_mod, date=attendance_date)
        attendance.save()
        for s in new_student_data:
            student = Student.objects.get(admin=s["id"])
            report = AttendanceReport(studentID=student, status=s["status"],attendanceID=attendance)
            report.save()
        return HttpResponse("Saved")
    except:
        return HttpResponse("Error")


# FUNCTIA PENTRU A RANDA PAGINA DE VERIFICARE SI VIZUALIZARE A PREZENTEI LA CURS   
def update_student_attendance(request):
    subjects = Subject.objects.filter(staffId = request.user.id)
    session = SessionYears.object.all()
    return render(request, "staff_templates/update_student_attendance.html", {"subjects": subjects, "session":session})


# CU ACEASTA FUNCTIE SE REALIZEAZA PRELUAREA DATEI SI A MATERIEI PENTRU VERIFICAREA PREZENTEI LA CURS
@csrf_exempt
def get_att_data(request):
    subject = request.POST.get("subject")
    subject_object = Subject.objects.get(id=subject)
    
    session = request.POST.get("session")
    session_object = SessionYears.object.get(id=session)
    
    attendance = Attendance.objects.filter(subjectID=subject_object,session_id=session_object)
    attendance_data_list = []
    
    for a in attendance:
        data={"id": a.id, "date": str(a.date), "session_id": a.session_id.id}
        attendance_data_list.append(data)
    return JsonResponse(json.dumps(attendance_data_list), safe=False)


# CU ACESTA FUNCTIE SE REALIZEAZA PREZENTAREA SI DISPLAYING-UL ELEVILOR IN DIV-UL DIN JOSUL CHENARULUI CU VERIFICAREA PREZENTEI
@csrf_exempt
def show_student_data(request):   
    attendance_date = request.POST.get("attendanceDate")
    attendance = Attendance.objects.get(id=attendance_date)
    print(attendance)
    report = AttendanceReport.objects.filter(attendanceID=attendance)
    data = []
    for r in report:
        r = {"id": r.studentID.admin.id, "name": f"{r.studentID.admin.first_name} {r.studentID.admin.last_name}", "status":r.status}
        data.append(r) 
        
    return JsonResponse(json.dumps(data),content_type="application/json", safe=False)

# CU ACESTA FUNCTIA SE REALIZEAZA UPDATAREA PREZENTEI IN CAZUL IN CARE FUSESE FACUTA GRESIT IN PRIMA INSTANTA
@csrf_exempt
def update_attendance_data(request):
    students_id = request.POST.get("students_id")
    attendance_date = request.POST.get("attendanceDate")
    attendance = Attendance.objects.get(id=attendance_date)

    new_student_data = json.loads(students_id)
    try:
        for s in new_student_data:
            student = Student.objects.get(admin=s["id"])
            report = AttendanceReport.objects.get(studentID=student,attendanceID=attendance)
            report.status=s['status'];
            report.save()
        return HttpResponse("Saved")
    except:
        return HttpResponse("Error")
    
# ACEASTA FUNCTIE ESTE FOLOSITA PENTRU A RANDA PAGINA DE FEEDBACK A STAFF-ULUI SI ULTERIOR PERMITE PAGINII SA FOLOESASCA MESAJELE DE FEEDBACK EXISTENTE IN BAZA DE DATE PENTRU A LE INCLUDE INTR UN TABEL
def staff_send_feedback(request):
    staff = Staff.objects.get(admin=request.user.id)
    feedback = FeedbackStaff.objects.filter(staffID=staff)
    return render(request, "staff_templates/staff_send_feedback.html", {"feedback": feedback})

# ACEASTA FUNCTIE ARE ROLUL DE A SALVA FEEDBACK UL STAFF ULUI IN BAZA DE DATE
def staff_feedback(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        feedback_msg = request.POST.get("feedbackMessage")
        staff = Staff.objects.get(admin = request.user.id)
        
        try:
            feedback = FeedbackStaff(staffID=staff, feedback=feedback_msg, feedbackReply="")
            feedback.save()
            messages.success(request, 'Your feedback has been sent!' )
            return HttpResponseRedirect(reverse("staff_send_feedback"))
        except:
            messages.error(request, 'The platform could not process the request. Try again!')
            return HttpResponseRedirect(reverse("staff_send_feedback"))


# ACEASTA FUNCTIE ESTE FOLOSITA PENTRU A RANDA PAGINA PENTRU CEREREA DE CONCEDIU SAU CEREREA DE A SI LUA LIBER A STAFF ULUI IN CAZUL UNEI PROBLEME PERSOANALE
def staff_applyfor_leave(request):
    staff = Staff.objects.get(admin=request.user.id)
    data  = LeaveReportStaff.objects.filter(staffID=staff)
    return render(request, "staff_templates/staff_leave_application.html", {"leaveData": data})

#  ACEASTA FUNCTIE ARE ROLUL DE A SALVA CEREREA DE CONCEDIU SAU DE PROBLEMA IN BAZA DE DATE
def staff_send_leave(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        leave_date = request.POST.get("leave_date")
        leave_reason = request.POST.get("leave_reason")
        
        staff = Staff.objects.get(admin=request.user.id)
        
        try:
            report = LeaveReportStaff(leaveDate=leave_date, staffID=staff,leaveMessage=leave_reason, status=0)
            report.save()
            messages.success(request, 'Your leave application has been sent and it will be reviewed by the principal!' )
            return HttpResponseRedirect('/staff_applyfor_leave')
        except:
            messages.error(request, 'The platform could not process the request. Try again!')
            return HttpResponseRedirect('/staff_applyfor_leave')
        
        

def staff_profile(request): 
    user = UserCustom.objects.get(id=request.user.id)
    staff = Staff.objects.get(admin=user)
    return render(request, "staff_templates/staff_profile.html", {"user":user, "staff":staff})

def staff_profile_save(request):
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
            staff = Staff.objects.get(admin=user.id)
            staff.address = address
            staff.save()
            messages.success(request, 'Profile information have been updated!')
            return HttpResponseRedirect(reverse('staff_profile'))
        except:
            messages.error(request,'The platform could not process the request. Try again!')
            return HttpResponseRedirect(reverse('staff_profile'))