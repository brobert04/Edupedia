from django.shortcuts import render
from django.urls import reverse
from schoolManagementApp.models import Staff, UserCustom
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.decorators import login_required

# def profile_picture(request):
#     if request.user.is_authenticated:
#         user1 = UserCustom.objects.get(id=request.user.id)
#     return {'user': user}