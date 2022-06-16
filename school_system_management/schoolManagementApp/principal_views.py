# ACEASTA PAGINA CONTINE FUNCTIILE NECESARE FUNCTIONARII PAGINI DE ADMIN/DIRECTOR
from unicodedata import name
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from itsdangerous import NoneAlgorithm

from schoolManagementApp.forms import AddCourse, AddStaff, AddStudent, EditCourse, EditStaff, EditStudent

from schoolManagementApp.models import Course, SessionYears, Staff, Student, Subject, UserCustom

# FUNCTIA PENTRU A RANDA PAGINA DE DASHBOARD A DIRECTORULUI/ADMINULUI
def principal_home(request):
    return render(request, 'principal_templates/home.html')

# FUNCTIA PENTRU A RANDA PAGINA DE ADAUGARE STAFF
def add_staff(request):
    form = AddStaff()
    return render(request, 'principal_templates/add_staff.html', {"form":form})

# FUNCTIA PENTRU A SALVA INFORMATIILE NOULUI MEMBRU STAFF ADAUGAT SI PENTRU A-L ADAUGA IN BAZA DE DATE
def save_staff_info(request):
    if request.method != "POST":
        return HttpResponse('<h1 style="color: red;">THIS METHOD IS NOT ALLLOWED</h1>')
    else:
        form = AddStaff(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
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
        form = AddStudent(request.POST, request.FILES)
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
        
        
            profile_pic = request.FILES['profilePic']
            fs = FileSystemStorage()
            filename  = fs.save(profile_pic.name, profile_pic)
            profile_pic_url  = fs.url(filename)
        
            try:   
                # CREEM UN NOU USER CUSTOM CU MODELUL USERCUSTOM DIN BAZA DE DATE LA CARE ADAUGAM SI ADRESA   
                user = UserCustom.objects.create_user(username=username, password=password, email=email, last_name=last_name,first_name=first_name, user_type=3)
                user.student.address = address
                course_object = Course.objects.get(id=course_id)
                user.student.courseId = course_object
                session_year = SessionYears.object.get(id=session_id)
                user.student.session_id = session_year 
                user.student.gender = gender
                user.student.profile_picture = profile_pic_url
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
    return render(request, "principal_templates/edit_staff.html", {"form":form,"id": staff_id, "username": staff.admin.username})

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
            email = email = form.cleaned_data['email']  
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


def manage_session(request):
    return render(request, "principal_templates/manage_session.html")


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