from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from schoolManagementApp.models import UserCustom

# Register your models here.
class UserModel(UserAdmin):
    pass

admin.site.register(UserCustom, UserModel)

