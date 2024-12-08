from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('cpf', 'date_birth', 'phone_number', 'benefits')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('cpf', 'date_birth', 'phone_number', 'benefits')}),
    )
    list_display = ('first_name', 'last_name', 'email', 'cpf', 'phone_number')
