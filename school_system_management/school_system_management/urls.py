from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from school_system_management import settings
from schoolManagementApp import views
from schoolManagementApp.views import showDemoPage, loginPage, getUserData, Logout


urlpatterns = [
    path('demo/', views.showDemoPage, name='DemoPage'),
    path('', views.loginPage, name='LoginPage'),
    path('admin/', admin.site.urls),
    path('login', views.Login),
    path('get_user_data', views.getUserData),
    path('logout', views.Logout)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
