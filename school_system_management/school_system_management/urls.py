from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from school_system_management import settings
from schoolManagementApp import views
from school_system_management import principal_views
from school_system_management.principal_views import principal_home
from schoolManagementApp.views import showDemoPage, loginPage, getUserData, Logout


urlpatterns = [
    path('demo/', views.showDemoPage, name='DemoPage'),
    path('', views.loginPage, name='LoginPage'),
    path('admin/', admin.site.urls),
    path('login', views.Login),
    path('get_user_data', views.getUserData),
    path('logout', views.Logout),
    path('principal_dashboard', principal_views.principal_home),
    path('add_staff', principal_views.add_staff ),
    path('save_staff_information', principal_views.save_staff_info),
    path('add_course', principal_views.add_course),
    path('save_course_information', principal_views.save_course_info),
    path('add_student', principal_views.add_student),
    path('save_student_information', principal_views.save_student_information),
    path('add_subject',principal_views.add_subject),
    path('save_subject_information', principal_views.save_subject_info),
    path('manage_staff', principal_views.manage_staff),
    path('manage_student', principal_views.manage_student),
    path('manage_course', principal_views.manage_course),
    path('manage_subjects' , principal_views.manage_subjects),
    path('edit_staff/<str:staff_id>', principal_views.edit_staff),
    path('edit_staff_information', principal_views.edit_staff_information),
    path('edit_student/<str:student_id>', principal_views.edit_student),
    path('edit_student_information', principal_views.edit_student_information)
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
