from urllib.request import Request
from django.contrib.auth import logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from schoolManagementApp.Email import Email
from django.contrib import messages
import requests
import json


def showDemoPage(request):
    return render(request, "demo.html")


def loginPage(request): 
    return render(request, "login-page.html")


def Login(request):
    # IN CAZUL IN CARE NU TRIMITEM UN FORMULAR CARE NU ARE METODA POST
    if request.method != 'POST':
        return HttpResponse('<h1>THIS METHOD IS NOT ALLOWED</h1>')
    # ALTFEL FOLOSIM DATELE INTRDOUSE IN FORMULAR SI REALIZAM AUTENTIFICAREA UTILIZATORULUI FOLOSINDU-NE DE FUNCTIA DIN EMAIL.PY
    else:
        # FACEM UN SCHIMB DE DATE CU API-UL DE CAPTCHA DE LA GOOGLE PENTRU A VERIFIOCA RASPUNUL USERULUI INAINTE DE A SE LOGA
        captcha_token = request.POST.get('g-recaptcha-response')
        captcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        captcha_secret_key = '6LceptAhAAAAAIrLGX3J44NxcbM4YihCfjUYnQR5'
        captcha_data = {"secret":captcha_secret_key, "response":captcha_token}
        server_response = requests.post(url=captcha_url, data=captcha_data)
        captcha_json = json.loads(server_response.text)

        if captcha_json['success'] == False:
            messages.error(request, 'Invalid Captcha')
            return HttpResponseRedirect('/')

        user = Email.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        # IN CAZUL IN CARE USERUL EXISTA, REALIZAM LOGAREA
        if user is not None:
            login(request, user)
            # DACA USERUL ESTE ADMIN, RANDAM PAGINA DE DASHBOARD A ADMINULUI
            if user.user_type == "1":
                return HttpResponseRedirect('principal_dashboard')
            # DACA USERUL ESTE PARTE A STAFF ULUI, RANDAM PAGINA DE DASHBOARD A STAFF ULUI
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse('staff_dashboard'))
            # DACA USERUL ESTE STUDENT, RANDAM PAGINA DE DASHBOARD A STUDENTULUI
            else:
                 return HttpResponseRedirect(reverse('student_dashboard'))
        else:
            messages.error(request, "The credentials are not correct. Try again!")
            return HttpResponseRedirect('/', )

def getUserData(request):
    if request.user is not None:
        return HttpResponse(f"User: {request.user.email}, UserType: {request.user.user_type}")
    else:
        HttpResponse('User is not logged in!')

def Logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def handle_404(request, exception):
    return render(request, "error_pages/404.html")

def handle_500(request):
    return render(request, "error_pages/500.html")

def handle_403(request, exception):
    return render(request, "error_pages/403.html")

def handle_400(request, exception):
    return render(request, "error_pages/400.html")
