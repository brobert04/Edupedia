from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from schoolManagementApp.models import UserCustom

def principal_home(request):
    return render(request, 'principal_templates/home.html')

def add_staff(request):
    return render(request, 'principal_templates/add_staff.html')

def save_staff_info(request):
    if request.method != "POST":
        return HttpResponse('<h1>THIS METHOD IS NOT ALLOWED</h1>')
    else:
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')  
        try:      
            user = UserCustom.objects.create_user(username=username, password=password, email=email, last_name=last_name,first_name=first_name, user_type=2)
            user.staff.address = address 
            user.save()
            messages.success(request, 'A new staff member has been added to the database!')
            return HttpResponseRedirect('/add_staff')
        except:
             messages.error(request, 'The platform could not process the request. Try again!')
             return HttpResponseRedirect('/add_staff')