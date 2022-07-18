from django.contrib.auth import logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
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


def handle_404(request, exception):
    return render(request, "error_pages/404.html")

def handle_500(request):
    return render(request, "error_pages/500.html")

def handle_403(request, exception):
    return render(request, "error_pages/403.html")

def handle_400(request, exception):
    return render(request, "error_pages/400.html")


def showFirebaseJs(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/9.9.0/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/9.9.0/firebase-messaging.js");' \
           'const firebaseConfig = {' \
                'apiKey: "AIzaSyD-0otDO4PwXo8NlH9JAf6eZvukq37BUIY",' \
                'authDomain: "edupedia-356412.firebaseapp.com",' \
                'projectId: "edupedia-356412",' \
                'storageBucket: "edupedia-356412.appspot.com",' \
                'messagingSenderId: "490620593166",' \
                'appId: "1:490620593166:web:97764f9b6fff13f960485f",' \
                'measurementId: "G-BFDRTSF6LE"' \
            '};'\
            'firebase.initializeApp(firebaseConfig);' \
            'const messaging = firebase.messaging();' \
            'messaging.setBackgroundMessageHandler(function(payload){' \
                'console.log(payload);' \
                'const notification = JSON.parse(payload)' \
                'const notificationOption={' \
                    'body:notification.body,' \
                    'icon:notification.icon,' \
                '};' \
            'return self.registration.showNotification(payload.notification.title, notificationOption)'\
            '})"'
    return HttpResponse(data)