from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from school_system_management import settings
from schoolManagementApp import views
from schoolManagementApp import principal_views
from schoolManagementApp.principal_views import principal_home
from schoolManagementApp.views import showDemoPage, loginPage, getUserData, Logout


urlpatterns = [
    path('demo/', views.showDemoPage, name='DemoPage'),
    path('', views.loginPage, name='LoginPage'),
    path('admin/', admin.site.urls, name="admin"),
    path('login', views.Login, name="login"),
    path('get_user_data', views.getUserData),
    path('logout', views.Logout, name="logout"),
    path('principal_dashboard', principal_views.principal_home, name="principal_dashboard"),
    path('add_staff', principal_views.add_staff, name="add_staff" ),
    path('save_staff_information', principal_views.save_staff_info, name="save_staff"),
    path('add_course', principal_views.add_course, name="add_course"),
    path('save_course_information', principal_views.save_course_info, name="save_course"),
    path('add_student', principal_views.add_student, name="add_student"),
    path('save_student_information', principal_views.save_student_information, name="save_student"),
    path('add_subject',principal_views.add_subject, name="add_subject"),
    path('save_subject_information', principal_views.save_subject_info, name="save_subject"),
    path('manage_staff', principal_views.manage_staff, name="manage_staff"),
    path('manage_student', principal_views.manage_student, name="manage_student"),
    path('manage_course', principal_views.manage_course, name="manage_course"),
    path('manage_subjects' , principal_views.manage_subjects, name="manage_subject"),
    
    path('edit_staff/<str:staff_id>', principal_views.edit_staff, name="edit_staff"),
    path('edit_staff_information', principal_views.edit_staff_information, name="edit_staff_information"),
    
    path('edit_student/<str:student_id>', principal_views.edit_student, name="edit_student"),
    path('edit_student_information', principal_views.edit_student_information, name="edit_student_information"),
    
    path('edit_course/<str:course_id>', principal_views.edit_course, name="edit_course"),
    path('edit_course_information', principal_views.edit_course_information, name="edit_course_information"),
    
    path('edit_subject/<str:subject_id>', principal_views.edit_subject, name="edit_subject"),    
    path('edit_subject_information', principal_views.edit_subject_information, name="edit_subject_information")
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
