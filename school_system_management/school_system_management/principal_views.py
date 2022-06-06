# ACEASTA PAGINA CONTINE FUNCTIILE NECESARE FUNCTIONARII PAGINI DE ADMIN/DIRECTOR
from unicodedata import name
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from schoolManagementApp.models import Course, Staff, Student, Subject, UserCustom

# FUNCTIA PENTRU A RANDA PAGINA DE DASHBOARD A DIRECTORULUI/ADMINULUI
def principal_home(request):
    return render(request, 'principal_templates/home.html')

# FUNCTIA PENTRU A RANDA PAGINA DE ADAUGARE STAFF
def add_staff(request):
    return render(request, 'principal_templates/add_staff.html')

# FUNCTIA PENTRU A SALVA INFORMATIILE NOULUI MEMBRU STAFF ADAUGAT SI PENTRU A-L ADAUGA IN BAZA DE DATE
def save_staff_info(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')  
        try:   
            # CREEM UN NOU USER CUSTOM CU MODELUL USERCUSTOM DIN BAZA DE DATE LA CARE ADAUGAM SI ADRESA   
            user = UserCustom.objects.create_user(username=username, password=password, email=email, last_name=last_name,first_name=first_name, user_type=2)
            user.staff.address = address 
            user.save()
            messages.success(request, 'A new staff member has been added to the database!')
            return HttpResponseRedirect('/add_staff')
        except:
             messages.error(request, 'The platform could not process the request. Try again!')
             return HttpResponseRedirect('/add_staff')

# FUNCTIA PENTRU A RANDA PAGINA DE ADAUGARE CURS       
def add_course(request):
    return render(request, 'principal_templates/add_course.html')


# FUNCTIA PENTRU A SALVA INFORMATIILE DESPRE CURS IN BAZA DE DATE
def save_course_info(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        course_name = request.POST.get('courseName')
        try:
            course = Course(name=course_name)
            course.save()
            messages.success(request, 'A new course has been added!')
            return HttpResponseRedirect('/add_course')
        except:
             messages.error(request, 'The platform could not process the request. Try again!')
             return HttpResponseRedirect('/add_course')

# FUNCTIA PENTRU A RANDA PAGINA DE ADAUGARE STUDENT
def add_student(request):
    courses = Course.objects.all()
    return render(request, 'principal_templates/add_student.html', {"courses":courses})

# FUNCTIA PENTRU A SALVA INFORMATIILE STUDENTULUI IN BAZA DE DATE
def save_student_information(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender  = request.POST.get('gender')
        startYear = request.POST.get('startDate')
        endYear = request.POST.get('endDate')
        course_id = request.POST.get('course')
        try:   
            # CREEM UN NOU USER CUSTOM CU MODELUL USERCUSTOM DIN BAZA DE DATE LA CARE ADAUGAM SI ADRESA   
            user = UserCustom.objects.create_user(username=username, password=password, email=email, last_name=last_name,first_name=first_name, user_type=3)
            user.student.address = address
            course_object = Course.objects.get(id=course_id)
            user.student.courseId = course_object 
            user.student.startYear = startYear
            user.student.finishYear = endYear
            user.student.gender = gender
            user.student.profile_picture = ""
            user.save()
            messages.success(request, 'A new student has been added to the database!')
            return HttpResponseRedirect('/add_student')
        except:
            messages.error(request, 'The platform could not process the request. Try again!')
            return HttpResponseRedirect('/add_student')
        
        
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
    staff = Staff.objects.get(admin=staff_id)
    return render(request, "principal_templates/edit_staff.html", {"staff": staff})

#FUNCTIA PENTRU A SALVA NOILE INFORMATII ALE STAFF ULUI
def edit_staff_information(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        staff_id = request.POST.get('staff_id')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')
        
        try:
            user  = UserCustom.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()
                
            staff = Staff.objects.get(admin=staff_id)
            staff.address = address
            staff.save()
            messages.success(request, 'Teacher information have been updated!')
            return HttpResponseRedirect(f"/edit_staff/{staff_id}")
        except:
            messages.error(request,'The platform could not process the request. Try again!')
            return HttpResponseRedirect(f"/edit_staff/{staff_id}")


# FUNCTIA PENTRU A RANDA PAGINA DE A UPDATA INFORMATIILE STUDENTULUI
def edit_student(request, student_id):
    courses = Course.objects.all()
    student = Student.objects.get(admin=student_id)
    return render(request, 'principal_templates/edit_student.html', {"student": student, "courses": courses})

#FUNCTIA PENTRU A SALVA NOILE INFORMATII ALE STUDENTULUI
def edit_student_information(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')
        course  = request.POST.get('course')
        # course_obj = course_object = Course.objects.get(id=course)
        gender = request.POST.get('gender')
        start_year = request.POST.get('startDate')
        end_year = request.POST.get('endDate')
        
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
            student.startYear = start_year
            student.finishYear = end_year
            course = Course.objects.get(id=course)
            student.courseId = course
            student.save()
            
            messages.success(request, 'Student information have been updated!')
            return HttpResponseRedirect(f"/edit_student/{student_id}")
        except:
            messages.error(request,'The platform could not process the request. Try again!')
            return HttpResponseRedirect(f"/edit_student/{student_id}")