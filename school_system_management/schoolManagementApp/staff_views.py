import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from requests import session

from schoolManagementApp.models import Attendance, AttendanceReport, SessionYears, Student, Subject
from  django.views.decorators.csrf import csrf_exempt
from django.core import serializers

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

    
def update_student_attendance(request):
    subjects = Subject.objects.filter(staffId = request.user.id)
    return render(request, "staff_templates/update_student_attendance.html", {"subjects": subjects})