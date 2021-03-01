from django.contrib import admin
from maintenance.models import Machine
# Register your models here.

class MachineAdmin(admin.ModelAdmin):
    list_display = ('id', 'machine_name', 'machine_number', 'machine_serial_number', 
                    'section')
    list_display_links = ('id', 'machine_name')
    list_filter = ('machine_name',)
    search_fields = ('machine_name', 'machine_number', 'machine_serial_number',)
    list_per_page = 25



admin.site.register(Machine, MachineAdmin)