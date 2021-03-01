from django.contrib import admin
from quality.models import (Profile_machines_matching, Coil_parameters, Reconsiliation,
                            Coil_description)

# Register your models here.


class Profile_machines_matchingAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'producing_machine')
    list_display_links = ('id', 'profile')
    list_filter = ('profile', 'producing_machine')
    # list_editable = ('is_published',)
    search_fields = ('id', 'profile', 'producing_machine')
    list_per_page = 25

admin.site.register(Profile_machines_matching, Profile_machines_matchingAdmin)

class Coil_parametersAdmin(admin.ModelAdmin):
    list_display = ('id', 'coil_type', 'coil_finish', 'coil_gauge', 'coil_thickness',
                    'coil_width', 'coil_constant')
    list_display_links = ('id', 'coil_type', 'coil_finish')
    list_filter = ('coil_type', 'coil_finish', 'coil_gauge',
                    'coil_thickness', 'coil_width')
    # list_editable = ('is_published',)
    search_fields = ('coil_type', 'coil_finish', 'coil_gauge',
                    'coil_thickness', 'coil_width')
    list_per_page = 25
admin.site.register(Coil_parameters, Coil_parametersAdmin)


class CoilDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'coil_type', 'coil_finish', 'coil_colour')
    list_display_links = ('id', 'coil_type', 'coil_colour')
    list_filter = ('coil_type', 'coil_finish', 'coil_colour')
    search_fields = ('coil_type', 'coil_finish', 'coil_colour')
    list_per_page = 25

admin.site.register(Coil_description, CoilDescriptionAdmin)

class ReconsiliationAdmin(admin.ModelAdmin):
    list_display = ("coil_number", "coil_gauge", "coil_width", "coil_colour", 
                    "coil_finish", "initial_running_meters","produced_running_meters", 
                    "running_meters_gain", "initial_mass", "produced_mass",
                    "mass_gain")
    list_display_links = ("coil_number", "coil_gauge")
    list_filter = ("coil_number", "coil_gauge", "coil_width", "coil_colour", 
                    "coil_finish")
    search_fields = ("coil_number", "coil_gauge", "coil_width", "coil_colour", 
                    "coil_finish")
    list_per_page = 25

admin.site.register(Reconsiliation, ReconsiliationAdmin)
