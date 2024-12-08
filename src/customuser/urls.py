from django.urls import path
from customuser import views

urlpatterns = [
    path("number/<str:number>", views.get_user_by_number)
]