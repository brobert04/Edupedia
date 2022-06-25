import django
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from school_system_management import settings
from schoolManagementApp import staff_views, student_views, views
from schoolManagementApp import principal_views
from schoolManagementApp.principal_views import principal_home
from schoolManagementApp.views import showDemoPage, loginPage, getUserData, Logout


urlpatterns = [
    path('demo/', views.showDemoPage, name='DemoPage'),
    path('', views.loginPage, name='LoginPage'),
    path('accounts/', include('django.contrib.auth.urls')),
    # ADMIN PAGE URLS
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
    path('edit_subject_information', principal_views.edit_subject_information, name="edit_subject_information"),
    path("manage_session", principal_views.manage_session, name="manage_session"),
    path('save_session_information', principal_views.save_session_information, name="save_session_information"),
    path("check_if_email_exist", principal_views.check_if_email_exist, name="check_if_email_exist"),
    path("check_if_username_exist", principal_views.check_if_username_exist, name="check_if_username_exist"),
    path("student_feedback_reply", principal_views.student_feedback_reply, name="student_feedback_reply"),
    path("staff_feedback_reply", principal_views.staff_feedback_reply, name="staff_feedback_reply"),
    path("student_feedback_reply_messasge", principal_views.student_feedback_reply_message, name="student_feedback_reply_message"),
    path("staff_feedback_reply_message", principal_views.staff_feedback_reply_message, name="staff_feedback_reply_message"),
    
    
    
    # STAFF PAGE URLS
    path('staff_dashboard', staff_views.staff_home, name="staff_dashboard"),
    path("student_attendance", staff_views.student_attendance, name="student_attendance"),
    path("update_student_attendance", staff_views.update_student_attendance, name="update_student_attendance"),
    path("get_students", staff_views.get_students, name="get_students"),
    path("attendance_data", staff_views.attendance_data, name="attendance_data"),
    path("get_att_data", staff_views.get_att_data, name="get_att_data"),
    path("show_student_data", staff_views.show_student_data, name="show_student_data"),
    path("update_attendance_data", staff_views.update_attendance_data, name="update_attendance_data"),
    path("staff_send_feedback", staff_views.staff_send_feedback, name="staff_send_feedback"),
    path("staff_feedback", staff_views.staff_feedback, name="staff_feedback"),
    path("staff_applyfor_leave", staff_views.staff_applyfor_leave, name="staff_applyfor_leave"),
    path("staff_send_leave", staff_views.staff_send_leave, name="staff_send_leave"),
    
    
    
    # STUDENT PAGE URLS
    path('student_dashboard', student_views.student_home, name="student_dashboard"),
    path('student_view_attendance', student_views.student_view_attendance, name="student_view_attendance"),
    path("student_view_attendance_data", student_views.student_view_attendance_data, name="student_view_attendance_data"),
    
    path("student_send_feedback", student_views.student_send_feedback, name="student_send_feedback"),
    path("student_feedback", student_views.student_feedback, name="student_feedback"),
    
    path("student_applyfor_leave", student_views.student_applyfor_leave, name="student_applyfor_leave"),
    path("student_send_leave", student_views.student_send_leave, name="student_send_leave"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
