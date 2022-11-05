# ACEASTA PAGINA CONTINE FUNCTIILE NECESARE FUNCTIONARII PAGINI DE ADMIN/DIRECTOR
from datetime import timedelta
import json
from unicodedata import name
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from httplib2 import Http
from  django.views.decorators.csrf import csrf_exempt
import httplib2
import requests

from schoolManagementApp.forms import AddCourse, AddStaff, AddStudent,EditCourse, EditStaff, EditStudent

from schoolManagementApp.models import Attendance, AttendanceReport, Course, FeedbackStaff, FeedbackStudent, LeaveReportStaff, LeaveReportStudent, SessionYears, Staff, Student, Subject, UserCustom, StudentNotification, StaffNotification

from notifications.signals import notify


# from google.oauth2 import service_account
# from django.views.generic import FormView
# from googleapiclient.discovery import build
# from oauth2client.service_account import ServiceAccountCredentials
# from googleapiclient.errors import HttpError


# service_account_email = "edupedia-google-calendar-event@edupedia-356412.iam.gserviceaccount.com"
# SCOPES = ["https://www.googleapis.com/auth/calendar"]
# scopes = [SCOPES]
# calendarId = "brb2iln1odddcmvm67nm13baf4@group.calendar.google.com"





# FUNCTIA PENTRU A RANDA PAGINA DE DASHBOARD A DIRECTORULUI/ADMINULUI
def principal_home(request):
    students_count = Student.objects.all().count()
    courses = Course.objects.all().count()
    subjects = Subject.objects.all().count()
    teachers = Staff.objects.all().count()
    
    
    all_courses = Course.objects.all()
    course_name = []
    subject_count = []
    student_count = []
    for course in all_courses:
        subj = Subject.objects.filter(courseId=course.id).count()
        students = Student.objects.filter(courseId = course.id).count()
        course_name.append(course.name)
        subject_count.append(subj)
        student_count.append(students)
        

    studs = Student.objects.all();
    studs_present_list = []
    studs_absent_list = []
    studs_name_list = []
    
    for s in studs:
        present = AttendanceReport.objects.filter(studentID=s.id, status=True).count()
        absent = AttendanceReport.objects.filter(studentID=s.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(studentID=s.id, status=1).count()
        studs_absent_list.append(absent+leaves)
        studs_present_list.append(present)
        studs_name_list.append(f"{s.admin.first_name} {s.admin.last_name}")
    return render(request, 'principal_templates/home.html', {"students": students_count, "courses": courses, "subjects": subjects, "teachers": teachers, "course_name": course_name, "subject_count": subject_count, "student_count":student_count, "student_present_list":studs_present_list, "student_absent_list":studs_absent_list, "student_name_list":studs_name_list})

# FUNCTIA PENTRU A RANDA PAGINA DE ADAUGARE STAFF
def add_staff(request):
    form = AddStaff()
    return render(request, 'principal_templates/add_staff.html', {"form":form})

# FUNCTIA PENTRU A SALVA INFORMATIILE NOULUI MEMBRU STAFF ADAUGAT SI PENTRU A-L ADAUGA IN BAZA DE DATE
def save_staff_info(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        form = AddStaff(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            phone_number = form.cleaned_data['phoneNumber']  
            
            profile_pic = request.FILES['profilePicture']
            fs = FileSystemStorage()
            filename  = fs.save(profile_pic.name, profile_pic)
            profile_pic_url  = fs.url(filename)      
            try:   
                # CREEM UN NOU USER CUSTOM CU MODELUL USERCUSTOM DIN BAZA DE DATE LA CARE ADAUGAM SI ADRESA   
                user = UserCustom.objects.create_user(username=username, password=password, email=email, last_name=last_name,first_name=first_name, user_type=2)
                user.staff.address = address 
                user.staff.gender = gender
                user.staff.phone_number = phone_number
                user.staff.profile_picture = profile_pic_url
                user.save()
                messages.success(request, 'A new staff member has been added to the database!')
                return HttpResponseRedirect('/add_staff')
            except:
                messages.error(request, 'The platform could not process the request. Try again!')
                return HttpResponseRedirect('/add_staff')
        else:
            form = AddStaff()
            return render(request, 'principal_templates/add_staff.html', {"form":form})


# FUNCTIA PENTRU A RANDA PAGINA DE ADAUGARE CURS       
def add_course(request):
    form = AddCourse()
    return render(request, 'principal_templates/add_course.html', {"form":form})


# FUNCTIA PENTRU A SALVA INFORMATIILE DESPRE CURS IN BAZA DE DATE
def save_course_info(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>') 
    else:
        form = AddCourse(request.POST)
        if form.is_valid():
            course_name = form.cleaned_data['courseName']
            try:
                course = Course(name=course_name)
                course.save()
                messages.success(request, 'A new course has been added!')
                return HttpResponseRedirect('/add_course')
            except:
                messages.error(request, 'The platform could not process the request. Try again!')
                return HttpResponseRedirect('/add_course')
        else:
            form = AddCourse()
            return render(request, 'principal_templates/add_course.html', {"form":form})
        
# FUNCTIA PENTRU A RANDA PAGINA DE ADAUGARE STUDENT
def add_student(request):
    form  = AddStudent()
    return render(request, 'principal_templates/add_student.html', {"form": form})

# FUNCTIA PENTRU A SALVA INFORMATIILE STUDENTULUI IN BAZA DE DATE
def save_student_information(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        form = AddStudent(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            gender  = form.cleaned_data['gender']
            session_id = form.cleaned_data['session_id']
            course_id = form.cleaned_data['course']
        
        
            try:   
                # CREEM UN NOU USER CUSTOM CU MODELUL USERCUSTOM DIN BAZA DE DATE LA CARE ADAUGAM SI ADRESA   
                user = UserCustom.objects.create_user(username=username, password=password, email=email, last_name=last_name,first_name=first_name, user_type=3)
                user.student.address = address
                course_object = Course.objects.get(id=course_id)
                user.student.courseId = course_object
                session_year = SessionYears.object.get(id=session_id)
                user.student.session_id = session_year 
                user.student.gender = gender
                user.save()
                messages.success(request, 'A new student has been added to the database!')
                return HttpResponseRedirect('/add_student')
            except:
                messages.error(request, 'The platform could not process the request. Try again!')
                return HttpResponseRedirect('/add_student')
        else:
            form=AddStudent(request.POST)
            return render(request, 'principal_templates/add_student.html', {"form": form})
            
        
# FUNCTIA PENTRU A RANDA PAGINA DE ADAUGARE MATERIE    
def add_subject(request):
    courses = Course.objects.all()
    staff = UserCustom.objects.filter(user_type=2)
    return render(request, 'principal_templates/add_subject.html', {"courses" : courses, "staff": staff})

# FUNCTIA PENTRU A SALVA DATELE DESPRE NOUA MATERIE   
def save_subject_info(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        subject_name = request.POST.get('subjectName')
        course_id = request.POST.get('course')
        course_object = Course.objects.get(id=course_id)
        teacher = request.POST.get('teacher')
        teacher_object = UserCustom.objects.get(id=teacher)
        try:
            subject = Subject(name=subject_name, courseId = course_object, staffId = teacher_object)
            subject.save()
            messages.success(request, 'A new subject has been added!')
            return HttpResponseRedirect('/add_subject')
        except:
             messages.error(request, 'The platform could not process the request. Try again!')
             return HttpResponseRedirect('/add_subject')
         
         
 # FUNCTIA PENTRU A RANDA PAGINA CU TOTI MEMBRII STAFF ULUI           
def manage_staff(request):
    staff = Staff.objects.all()
    return render(request, 'principal_templates/manage_staff.html', {"staff" : staff})

 # FUNCTIA PENTRU A RANDA PAGINA CU TOTI STUDENTII  
def manage_student(request):
    student = Student.objects.all()
    return render(request, 'principal_templates/manage_student.html', {"students": student})

 # FUNCTIA PENTRU A RANDA PAGINA CU TOATE CURSURILE
def manage_course(request):
    course = Course.objects.all()
    return render(request, 'principal_templates/manage_course.html', {"courses": course})

 # FUNCTIA PENTRU A RANDA PAGINA CU TOATE MATERIILE
def manage_subjects(request):
    subject = Subject.objects.all()
    return render(request,'principal_templates/manage_subject.html', {"subjects": subject})

# FUNCTIA PENTRU A RANDA PAGINA DE A UPDATA INFORMATIILE STAFF-ULUI
def edit_staff(request, staff_id):
    request.session['staff_id'] = staff_id
    staff = Staff.objects.get(admin=staff_id)
    form = EditStaff()
    form.fields['firstName'].initial = staff.admin.first_name
    form.fields['lastName'].initial = staff.admin.last_name
    form.fields['username'].initial = staff.admin.username
    form.fields['address'].initial = staff.address
    form.fields['email'].initial = staff.admin.email
    form.fields["phoneNumber"].initial = staff.phone_number
    form.fields["gender"].initial = staff.gender
    return render(request, "principal_templates/edit_staff.html", {"form":form,"id": staff_id, "username": staff.admin.username})

# FUNCTIA PENTRU A STERGE UN MEMBRU AL STAFF-ULUI
def delete_staff(request, staff_id):
    staff = UserCustom.objects.get(id=staff_id)
    staff.delete()
    return HttpResponseRedirect(reverse("manage_staff"))

#FUNCTIA PENTRU A SALVA NOILE INFORMATII ALE STAFF ULUI
def edit_staff_information(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        staff_id = request.session.get('staff_id')
        if staff_id == None:
            return HttpResponseRedirect('/manage_staff')
        form = EditStaff(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            gender =  form.cleaned_data['gender']
            phone_number = form.cleaned_data['phoneNumber']
            
            if request.FILES.get('profilePic', False):
                profile_pic = request.FILES['profilePic']
                fs = FileSystemStorage()
                filename  = fs.save(profile_pic.name, profile_pic)
                profile_pic_url  = fs.url(filename)
            else:
                profile_pic_url = None
                
            try:
                user  = UserCustom.objects.get(id=staff_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()
                    
                staff = Staff.objects.get(admin=staff_id)
                staff.address = address
                staff.gender = gender 
                staff.phone_number = phone_number
                if profile_pic_url != None:
                    staff.profile_picture = profile_pic_url
                staff.save()
                del request.session['staff_id']
                messages.success(request, 'Teacher information have been updated!')
                return HttpResponseRedirect(f"/edit_staff/{staff_id}")
            except:
                messages.error(request,'The platform could not process the request. Try again!')
                return HttpResponseRedirect(f"/edit_staff/{staff_id}")
        else:
            form = EditStaff()
            staff = Staff.objects.get(admin=staff_id)
            return render(request, "principal_templates/edit_staff.html", {"form":form,"id": staff_id, "username": staff.admin.username})

# FUNCTIA PENTRU A RANDA PAGINA DE A UPDATA INFORMATIILE STUDENTULUI
def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Student.objects.get(admin=student_id)
    form = EditStudent()
    form.fields['firstName'].initial = student.admin.first_name
    form.fields['lastName'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['firstName'].initial = student.admin.first_name
    form.fields['gender'].initial = student.gender
    form.fields['email'].initial = student.admin.email
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.courseId.id
    form.fields['course'].initial = student.courseId.id
    form.fields['session_id'].initial = student.session_id.id
    
    return render(request, 'principal_templates/edit_student.html', {"form":form, "id":student_id,"username": student.admin.username})

def delete_student(request, student_id):
    student = UserCustom.objects.get(id=student_id)
    student.delete()
    return HttpResponseRedirect(reverse("manage_student"))

#FUNCTIA PENTRU A SALVA NOILE INFORMATII ALE STUDENTULUI
def edit_student_information(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        student_id = request.session.get('student_id')
        if student_id==None:
            return HttpResponseRedirect('/manage_student')
        
        form = EditStudent(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            course  = form.cleaned_data['course']
            gender = form.cleaned_data['gender']
            session_id = form.cleaned_data['session_id']
            
            if request.FILES.get('profilePic', False):
                profile_pic = request.FILES['profilePic']
                fs = FileSystemStorage()
                filename  = fs.save(profile_pic.name, profile_pic)
                profile_pic_url  = fs.url(filename)
            else:
                profile_pic_url = None
            
            try:
                user = UserCustom.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()
                
                student  = Student.objects.get(admin=student_id)
                student.address = address
                student.gender = gender
                session_year = SessionYears.object.get(id=session_id)
                student.session_id = session_year
                if profile_pic_url != None:
                    student.profile_picture = profile_pic_url
                course = Course.objects.get(id=course)
                student.courseId = course
                student.save()
                del request.session['student_id']
                
                messages.success(request, 'Student information have been updated!')
                return HttpResponseRedirect(f"/edit_student/{student_id}")
            except:
                messages.error(request,'The platform could not process the request. Try again!')
                return HttpResponseRedirect(f"/edit_student/{student_id}")
        else:
            form=EditStudent(request.POST)
            student=Student.objects.get(admin=student_id)
            return render(request, "principal_templates/edit_student.html", {"form": form, "id": student_id, "username": student.admin.username})
        

# FUNCTIA PENTRU A RANDA PAGINA DE A UPDATA INFORMATIILE DESPRE CURS
def edit_course(request, course_id):
    request.session['course_id'] = course_id
    course  = Course.objects.get(id=course_id)
    form = EditCourse()
    form.fields['courseName'].initial = course.name
    return render(request, "principal_templates/edit_course.html", {"name": course.name, "id": course_id, "form":form})

def delete_course(request, course_id):
    course = Course.objects.get(id = course_id)
    course.delete()
    return HttpResponseRedirect(reverse("manage_course"))

#FUNCTIA PENTRU A SALVA NOILE INFORMATII REFERITOARE LA CURS
def edit_course_information(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        course_id = request.session['course_id']
        if course_id ==None:
            HttpResponseRedirect('/manage_subject')
        
        
        form = EditCourse(request.POST)
        if form.is_valid():
            course_name = form.cleaned_data['courseName']
            
            try:
                course = Course.objects.get(id=course_id)        
                course.name = course_name
                course.save()
                messages.success(request, 'Course information have been updated!')
                return HttpResponseRedirect(f"/edit_course/{course_id}")
            except:
                messages.error(request,'The platform could not process the request. Try again!')
                return HttpResponseRedirect(f"/edit_course/{course_id}")
        else:
            pass



# FUNCTIA PENTRU A RANDA PAGINA DE A UPDATA INFORMATIILE DESPRE MATERIE
def edit_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    course = Course.objects.all()
    teachers = UserCustom.objects.filter(user_type=2)
    return render(request, 'principal_templates/edit_subject.html', {"subject": subject, "courses": course, "teachers": teachers, "id": subject_id})

#FUNCTIA PENTRU A SALVA NOILE INFORMATII REFERITOARE LA MATERIE
def edit_subject_information(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subjectName')
        course_name = request.POST.get('course')
        teacher = request.POST.get('teacher')
        
        try:
            subject = Subject.objects.get(id=subject_id)        
            subject.name = subject_name
            staff = UserCustom.objects.get(id=teacher)
            subject.staffId = staff
            course = Course.objects.get(id=course_name)
            subject.courseId = course
            subject.save()
            messages.success(request, 'Subject information have been updated!')
            return HttpResponseRedirect(f"/edit_subject/{subject_id}")
        except:
            messages.error(request,'The platform could not process the request. Try again!')
            return HttpResponseRedirect(f"/edit_subject/{subject_id}")


# FUNCTIA PENRU A RANDA PAGINA DE SELECTARE A DURATEI SESIUNII
def manage_session(request):
    return render(request, "principal_templates/manage_session.html")


# FUNCTIA PENTRU A SALVA INFORMATIILE DESPRE NOUA SESIUNE IN BAZA DE DATE
def save_session_information(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        session_start = request.POST.get('sessionStart')
        session_end = request.POST.get('sessionEnd') 
        
        try:
            session  = SessionYears(startYear=session_start, endYear=session_end)
            session.save()
            messages.success(request, 'Session information have been saved!')
            return HttpResponseRedirect(reverse(manage_session))
        except:
            messages.error(request,'The platform could not process the request. Try again!')
            return HttpResponseRedirect(reverse('manage_sesion'))
        

# ACESTA DOUA FUNCTII SUNT UTILIZATE PENTRU A VERIFICA DACA USERNAME UL SI EMAIL UL AU MAI FOST ASOCIATE ALTUI CONT
@csrf_exempt
def check_if_email_exist(request):
    email  = request.POST.get("email")
    user = UserCustom.objects.filter(email=email).exists()
    if user:
        return HttpResponse(True)
    else:
         return HttpResponse(False)
     
     
@csrf_exempt
def check_if_username_exist(request):
    username  = request.POST.get("username")
    user = UserCustom.objects.filter(username=username).exists()
    if user:
        return HttpResponse(True)
    else:
         return HttpResponse(False)



# ACESTE PATRU FUNCTII SUNT RESPONSABILE PENTRU POSIBILITATEA ADMINULUI DE A RASPUNDE LA FEEDBACK UL ADRESAT DE STAFF SI STUDENT DIRECTORULUI
def staff_feedback_reply(request):
    feedback = FeedbackStaff.objects.all()
    return render(request, "principal_templates/staff_feedback_template.html", {"feedback": feedback})

@csrf_exempt
def staff_feedback_reply_message(request):
    feedback_id = request.POST.get("id")
    feedback_message  = request.POST.get("message")
    
    try:
        feedback  = FeedbackStaff.objects.get(id=feedback_id)
        feedback.feedbackReply = feedback_message;
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False") 
    


def student_feedback_reply(request):
    feedback = FeedbackStudent.objects.all()
    return render(request, "principal_templates/student_feedback_template.html", {"feedback": feedback})


@csrf_exempt
def student_feedback_reply_message(request):
    feedback_id = request.POST.get("id")
    feedback_message  = request.POST.get("message")
    try:
        feedback  = FeedbackStudent.objects.get(id=feedback_id)
        feedback.feedbackReply = feedback_message;
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False") 
    
    


def student_leave_request(request):
    requests = LeaveReportStudent.objects.all();
    return render(request, "principal_templates/student_leave_request.html", {"request": requests})

def approve_student_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.status = 1
    leave.save()
    return HttpResponseRedirect(reverse('student_leave_request'))

def reject_student_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.status = 2
    leave.save()
    return HttpResponseRedirect(reverse('student_leave_request'))


def staff_leave_request(request):
    requests = LeaveReportStaff.objects.all()
    return render(request, "principal_templates/staff_leave_request.html", {"request": requests})


def approve_staff_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.status = 1
    leave.save()
    return HttpResponseRedirect(reverse('staff_leave_request'))


def reject_staff_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.status = 2
    leave.save()
    return HttpResponseRedirect(reverse('staff_leave_request'))



def principal_view_attendance_data(request):
    subjects = Subject.objects.all()
    session = SessionYears.object.all()
    return render(request, "principal_templates/view_student_attendance_report.html", {"subjects": subjects, "session":session})


@csrf_exempt
def admin_get_att_data(request):
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

@csrf_exempt
def admin_show_student_data(request):
    attendance_date = request.POST.get("attendanceDate")
    attendance = Attendance.objects.get(id=attendance_date)
    print(attendance)
    report = AttendanceReport.objects.filter(attendanceID=attendance)
    data = []
    for r in report:
        r = {"id": r.studentID.admin.id, "name": f"{r.studentID.admin.first_name} {r.studentID.admin.last_name}", "status":r.status}
        data.append(r) 
        
    return JsonResponse(json.dumps(data),content_type="application/json", safe=False)



def admin_profile(request):
    user = UserCustom.objects.get(id=request.user.id)
    return render(request, "principal_templates/admin_profile.html", {"user": user})

def edit_profile_save(request):
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
            return HttpResponseRedirect(reverse('admin_profile'))
        except:
            messages.error(request,'The platform could not process the request. Try again!')
            return HttpResponseRedirect(reverse('admin_profile'))
        

# def calendar(request):
#         form = CalendarForm();
#         return render(request, "principal_templates/calendar.html", {"form": form})
    
    
# def build_service(request):
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(filename="schoolManagementApp/service-account", scopes=SCOPES)
#     http = credentials.authorize(httplib2.Http())
#     service = build("calendar", "v3", http=http)
#     return service

# def save_event(request):
#     if request.method != "POST":
#         return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
#     else:
#         form = CalendarForm(request.POST)
#         if form.is_valid():
#             eventTitle = form.cleaned_data.get('eventTitle')
#             startDate = form.cleaned_data.get('startDateTime')
#             endDate = form.cleaned_data.get('endDateTime')
#             description = form.cleaned_data.get('description')
#             service = build_service(request)
#             event = (
#             service.events().insert(
#                     calendarId=calendarId,
#                     body={
#                         "summary": eventTitle,
#                         "description": description,
#                         "start": {"dateTime": startDate.isoformat() + 'Z', "timeZone": "Europe/Amsterdam"},
#                         "end": {"dateTime": (startDate + timedelta(minutes=15)).isoformat()+ 'Z', "timeZone": "Europe/Amsterdam"},
#                     },
#                 ).execute()
#                 )
#             messages.success(request, 'Event added successfully.')
#             return HttpResponseRedirect(reverse('calendar'))
        
#         else:
#             print(form.errors)

def send_notification_student(request):
    student = Student.objects.all()
    return render(request, "principal_templates/send_notification_student.html", {"student": student})

def send_notification_staff(request):
    staff = Staff.objects.all()
    return render(request, "principal_templates/send_notification_staff.html", {"staff": staff})


@csrf_exempt
def send_student_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    sender = request.POST.get("sender")
    student = Student.objects.get(admin=id)
    notification = StudentNotification(studentID=student, message=message,sender=sender)
    notification.save()
    return HttpResponse("True")


@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    sender = request.POST.get("sender")
    staff = Staff.objects.get(admin=id)
    notification = StaffNotification(staffID=staff, message=message, sender=sender)
    notification.save()
    return HttpResponse("True")