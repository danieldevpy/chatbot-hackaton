from django.contrib import admin
from .models import TransportationVoucher, MealVoucher

@admin.register(TransportationVoucher)
class ValeTransporteAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_amount')

@admin.register(MealVoucher)
class ValeRefeicaoAdmin(admin.ModelAdmin):
    list_display = ('name', 'value_per_meal', 'quantity_of_meals')
