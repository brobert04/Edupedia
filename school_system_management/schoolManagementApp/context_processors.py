from django.shortcuts import render
from django.urls import reverse
from schoolManagementApp.models import Staff, UserCustom
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.decorators import login_required
import avinit

# def profile_picture(request):
#     if request.user.is_authenticated:
#         user1 = UserCustom.objects.get(id=request.user.id)
#     return {'user': user}

def profile_picture(request):
    try:
        user = request.user
        profile_pic = avinit.get_avatar_data_url(f"{user.first_name} {user.last_name}")
        return {"profile_picture" : profile_pic}
    except:
        return {"profile_picture" : ""}