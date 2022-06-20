# IN ACEST FILE CREEM UN MIDDLEWARE(https://bit.ly/39i1DqI) PENTRU A NU LASA STUDENTUL, DE EX, SA ACCESEZE PAGINILE ADMINULUI/STAFF-ULUI SI VICEVERSA. CU ALTE CUVINTE, ATUNCI CAND UN USER EFECTUEAZA UN REQUEST, MAI INTAI VA FI INTAMPINAT DE MIDDLEWARE SI MAI APOI VA PRIMI RASPUNSUL(IN CAZUL ASTA, REDIRECTIONAREA CATRE PAGINA DESTINATA LUI)

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self,request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_authenticated:
             # DACA USERUL ARE STATUT DE DIRECTOR/ADMIN POATE ACCESA NUMAI PAGINILE SPECIFICE DIRECTORULUI
            if user.user_type == "1":
                if modulename == "schoolManagementApp.principal_views":
                    pass
                elif modulename == "schoolManagementApp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("principal_dashboard"))
            
            # DACA USERUL ARE STATUT DE STAFF POATE ACCESA NUMAI PAGINILE SPECIFICE MEMBRILOR STAFFULUI    
            elif user.user_type == "2":
                if modulename == "schoolManagementApp.staff_views":
                    pass
                elif modulename == "schoolManagementApp.views"  or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_dashboard"))
                
             # DACA USERUL ARE STATUT DE STUDENT POATE ACCESA NUMAI PAGINILE SPECIFICE STUDENTILO    
            elif user.user_type == "3":
                if modulename == "schoolManagementApp.student_views":
                    pass
                elif modulename == "schoolManagementApp.views"  or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_dashboard"))
            else:
                return HttpResponseRedirect(reverse("LoginPage")) 
            
        # DACA USERUL NU ESTE AUTENTIFICAT, IL REDIRECTIONAM PENTRU A O REALIZA
        else:
            if request.path == reverse("LoginPage") or request.path == reverse("login") or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("LoginPage"))