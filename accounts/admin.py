from django.contrib import admin
from accounts.models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "employee_code", "department",
                    "section")
    list_display_links = ("id", "employee_code", "first_name")
    list_filter = ("employee_code", "section", "department")
    list_per_page = 25


admin.site.register(Employee, EmployeeAdmin)