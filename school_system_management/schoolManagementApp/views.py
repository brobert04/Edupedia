from django.contrib.auth import logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from schoolManagementApp.Email import Email
from django.contrib import messages


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
        user = Email.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))

        # IN CAZUL IN CARE USERUL EXISTA, REALIZAM LOGAREA
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('principal_dashboard')
        else:
            messages.error(request, "Datele introduse nu sunt corecte. Inecearca din nou!")
            return HttpResponseRedirect('/', )

def getUserData(request):
    if request.user is not None:
        return HttpResponse(f"User: {request.user.email}, UserType: {request.user.user_type}")
    else:
        HttpResponse('User is not logged in!')

def Logout(request):
    logout(request)
    return HttpResponseRedirect("/")