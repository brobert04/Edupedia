import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from requests import session
from schoolManagementApp.forms import EditStaff, StaffOwnProfileEdit
from schoolManagementApp.models import Attendance, AttendanceReport, Course, FeedbackStaff, LeaveReportStaff, SessionYears, Staff, StaffTodo, Student, Subject, UserCustom
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# FUNCTIA PENTRU A RANDA PAGINA DE DASHBOARD A MEMBRULUI STAFF-ULUI


def staff_home(request):
    # PRELUAM DATELE DESPRE STUDENTI AFLATI LA CURSUL PROFESORULUI IN CAUZA
    subject = Subject.objects.filter(staffId=request.user.id)
    course_ids_list = []
    for s in subject:
        course = Course.objects.get(id=s.courseId.id)
        course_ids_list.append(course.id)

    course_list = []
    # acest if va sterge id-urile duplicate ale cursurilor
    for course_id in course_ids_list:
        if course_id not in course_list:
            course_list.append(course_id)
    all_students = Student.objects.filter(courseId__in=course_list).count()

    attendance_count = Attendance.objects.filter(subjectID__in=subject).count()

    staff = Staff.objects.get(admin=request.user.id)
    profile_picture = staff.profile_picture
    leave_request_count = LeaveReportStaff.objects.filter(
        staffID=staff).count()
    accepted_requests = LeaveReportStaff.objects.filter(
        staffID=staff, status=1).count()
    rejected_requests = LeaveReportStaff.objects.filter(
        staffID=staff, status=2).count()
    pending_requests = LeaveReportStaff.objects.filter(
        staffID=staff, status=0).count()
    my_subjects = subject.count()

    todos = StaffTodo.objects.filter(staffID=staff)

    try:
        message = FeedbackStaff.objects.filter(staffID=staff).last().feedback
        reply = FeedbackStaff.objects.filter(
            staffID=staff).last().feedbackReply
    except:
        message = ""
        reply = ""

    return render(request, 'staff_templates/home.html', {"subject": subject, "all_students": all_students, "attendance_count": attendance_count, "leave_request": leave_request_count, "my_subjects": my_subjects, "feedback": message, "feedback_reply": reply, "accepted_requests": accepted_requests, "rejected_requests": rejected_requests, "pending_requests": pending_requests, "profile_picture": profile_picture, "todos": todos})

# FUNCTIA PENTRU A RANDA PAGINA DE STABILIRE A PREZENTEI LA CURS


def student_attendance(request):
    user = UserCustom.objects.get(id=request.user.id)
    subjects = Subject.objects.filter(staffId=user)
    profile_picture = user.staff.profile_picture
    session = SessionYears.object.all()
    return render(request, 'staff_templates/student_attendance.html', {"subjects": subjects, "session": session, "profile_picture": profile_picture})


# FOLOSIM AJAX PENTRU A DETERMINA ELEVII PREZENTI LA MATERIA RESPECTIVA SI PREZENTI IN ACEA SESIUNE
@csrf_exempt
def get_students(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')

    subject = Subject.objects.get(id=subject_id)
    session = SessionYears.object.get(id=session_id)
    student = Student.objects.filter(
        courseId=subject.courseId, session_id=session)
    data = []
    for s in student:
        d = {"id": s.admin.id, "name": f"{s.admin.first_name} {s.admin.last_name}"}
        data.append(d)
    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)


# PRELUAM DATELE REFERIOTOARE LA PREZENTA DIN DIV-UL RANDAT DINAMIC DIN PARGINA 'STUDENT_ATTENDANCE.HTML' SI LE SALVAM IN MODELUL DE PREZENTA 'ATTENDANCE'. ULTERIOR, PE BAZA ACESTOR INFORMATII, CREEZ SI RAPORTUL DE PREZENTA
@csrf_exempt
def attendance_data(request):
    students_id = request.POST.get("students_id")
    attendance_date = request.POST.get("attendanceDate")
    subject_id = request.POST.get("subject_id")
    session_id = request.POST.get("session_id")

    sub_mod = Subject.objects.get(id=subject_id)
    sess_mod = SessionYears.object.get(id=session_id)
    new_student_data = json.loads(students_id)
    try:
        attendance = Attendance(
            subjectID=sub_mod, session_id=sess_mod, date=attendance_date)
        attendance.save()
        for s in new_student_data:
            student = Student.objects.get(admin=s["id"])
            report = AttendanceReport(
                studentID=student, status=s["status"], attendanceID=attendance)
            report.save()
        return HttpResponse("Saved")
    except:
        return HttpResponse("Error")


# FUNCTIA PENTRU A RANDA PAGINA DE VERIFICARE SI VIZUALIZARE A PREZENTEI LA CURS
def update_student_attendance(request):
    subjects = Subject.objects.filter(staffId=request.user.id)
    session = SessionYears.object.all()
    return render(request, "staff_templates/update_student_attendance.html", {"subjects": subjects, "session": session})


# CU ACEASTA FUNCTIE SE REALIZEAZA PRELUAREA DATEI SI A MATERIEI PENTRU VERIFICAREA PREZENTEI LA CURS
@csrf_exempt
def get_att_data(request):
    subject = request.POST.get("subject")
    subject_object = Subject.objects.get(id=subject)

    session = request.POST.get("session")
    session_object = SessionYears.object.get(id=session)

    attendance = Attendance.objects.filter(
        subjectID=subject_object, session_id=session_object)
    attendance_data_list = []

    for a in attendance:
        data = {"id": a.id, "date": str(a.date), "session_id": a.session_id.id}
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
        r = {"id": r.studentID.admin.id,
             "name": f"{r.studentID.admin.first_name} {r.studentID.admin.last_name}", "status": r.status}
        data.append(r)

    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)

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
            report = AttendanceReport.objects.get(
                studentID=student, attendanceID=attendance)
            report.status = s['status']
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
        staff = Staff.objects.get(admin=request.user.id)

        try:
            feedback = FeedbackStaff(
                staffID=staff, feedback=feedback_msg, feedbackReply="")
            feedback.save()
            messages.success(request, 'Your feedback has been sent!')
            return HttpResponseRedirect(reverse("staff_send_feedback"))
        except:
            messages.error(
                request, 'The platform could not process the request. Try again!')
            return HttpResponseRedirect(reverse("staff_send_feedback"))


# ACEASTA FUNCTIE ESTE FOLOSITA PENTRU A RANDA PAGINA PENTRU CEREREA DE CONCEDIU SAU CEREREA DE A SI LUA LIBER A STAFF ULUI IN CAZUL UNEI PROBLEME PERSOANALE
def staff_applyfor_leave(request):
    staff = Staff.objects.get(admin=request.user.id)
    data = LeaveReportStaff.objects.filter(staffID=staff)
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
            report = LeaveReportStaff(
                leaveDate=leave_date, staffID=staff, leaveMessage=leave_reason, status=0)
            report.save()
            messages.success(
                request, 'Your leave application has been sent and it will be reviewed by the principal!')
            return HttpResponseRedirect('/staff_applyfor_leave')
        except:
            messages.error(
                request, 'The platform could not process the request. Try again!')
            return HttpResponseRedirect('/staff_applyfor_leave')


def staff_profile(request):
    user = UserCustom.objects.get(id=request.user.id)
    staff = Staff.objects.get(admin=user)
    gender = staff.gender
    address = staff.address
    phone = staff.phone_number
    profile_picture = staff.profile_picture
    subjects = Subject.objects.filter(staffId=user)
    course_ids_list = []
    for s in subjects:
        course = Course.objects.get(id=s.courseId.id)
        course_ids_list.append(course.id)

    course_list = []
    # acest if va sterge id-urile duplicate ale cursurilor
    for course_id in course_ids_list:
        if course_id not in course_list:
            course_list.append(course_id)
    all_students = Student.objects.filter(courseId__in=course_list).count()
    return render(request, "staff_templates/staff_profile.html", {"user": user, "staff": staff, "subjects": subjects, "all_students": all_students, "gender": gender, "address": address, "profile_picture": profile_picture, "phone": phone})


def edit_staff_profile(request):
    staff_id = request.user.id
    staff = Staff.objects.get(admin=staff_id)
    form = StaffOwnProfileEdit()
    form.fields['username'].initial = staff.admin.username
    form.fields['email'].initial = staff.admin.email
    form.fields['firstName'].initial = staff.admin.first_name
    form.fields['lastName'].initial = staff.admin.last_name
    form.fields['address'].initial = staff.address
    form.fields['phoneNumber'].initial = staff.phone_number
    return render(request, "staff_templates/edit_staff_profile.html", {"form": form})


def staff_profile_save(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        staff_id = request.user.id
        if staff_id is None:
            return HttpResponseRedirect(reverse("staff_profile"))
        form = StaffOwnProfileEdit(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            last_name = form.cleaned_data['lastName']
            address = form.cleaned_data['address']
            phoneNumber = form.cleaned_data['phoneNumber']

            if request.FILES.get('profilePicture', False):
                profile_pic = request.FILES['profilePicture']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
            try:
                user = UserCustom.objects.get(id=staff_id)
                user.username = username
                user.last_name = last_name
                user.save()

                staff = Staff.objects.get(admin=user)
                staff.address = address
                staff.phone_number = phoneNumber
                if profile_pic_url is not None:
                    staff.profile_picture = profile_pic_url
                staff.save()
                messages.success(
                    request, 'Profile information have been updated!')
                return HttpResponseRedirect(reverse("edit_staff_profile"))
            except:
                messages.error(
                    request, 'The platform could not process the request. Try again!')
                return HttpResponseRedirect(reverse("edit_staff_profile"))
        else:
            print(form.errors)


def add_todo_staff(request):
    task = request.POST.get("todoText")
    staff = Staff.objects.get(admin=request.user.id)
    new_todo = StaffTodo(task_text=task, staffID=staff)
    new_todo.save()
    return HttpResponseRedirect(reverse("staff_dashboard"))


def delete_todo_staff(request, todo_id):
    task = StaffTodo.objects.get(id=todo_id)
    task.delete()
    return HttpResponseRedirect(reverse("staff_dashboard"))


@csrf_exempt
def save_fcm_token_staff(request):
    token = request.POST.get("token")
    try:
        staff = Staff.objects.get(admin=request.user.id)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("Error")

