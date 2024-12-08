from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from .models import CustomUser

def get_user_by_number(request, number):
    user = get_object_or_404(CustomUser, phone_number=number)
    return JsonResponse(user.json(), status=200)