from django.contrib import admin
from .models import Medicine, Manufacturer, Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "total_amount", "status", "isPaid"]

@admin.register(Manufacturer)
class ManuFacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "contact_info"]

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price"]