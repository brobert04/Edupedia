import json
from django.http import JsonResponse
from django.shortcuts import render
from requests import session

from schoolManagementApp.models import SessionYears, Student, Subject
from  django.views.decorators.csrf import csrf_exempt
from django.core import serializers


def staff_home(request):
    return render(request, 'staff_templates/home.html')

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