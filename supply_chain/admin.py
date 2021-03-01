from django.contrib import admin
from .models import Coil, Inventory

# Register your models here.
class CoilAdmin(admin.ModelAdmin):
    list_display = ('id', 'coil_number',  'coil_gauge', 'coil_width',
                    'coil_colour','coil_finish','initial_mass','initial_running_meters', 
                    'date_received', 'coil_status', 'location')

    list_display_links = ('id', 'coil_number')
    list_filter = ('coil_number', 'coil_gauge', 'coil_width','coil_finish', 'coil_colour')
    search_fields = ('coil_number', 'initial_running_meters', 'initial_mass',)
    list_per_page = 25

admin.site.register(Coil, CoilAdmin)

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date','gauge', 'width',
                    'colour','finish', 'bond_inventory', 'transferred', 'production_stock')
    list_display_links = ('id', 'date' , 'gauge')
    list_filter = ('date','gauge', 'width', 'colour','finish')
    search_fields = ('date','gauge', 'width', 'colour','finish')
    list_per_page = 25

admin.site.register(Inventory, InventoryAdmin)