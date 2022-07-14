from django.shortcuts import render
from django.urls import reverse
from schoolManagementApp.models import Staff, UserCustom
from django.utils.functional import SimpleLazyObject


# def profile_picture(request):
#     user  = UserCustom.objects.get(id=request.user.id, user_type=2)
#     profile = user.profile_picture
#     return {'profile_picture': profile}