from django.contrib import admin
from production.models import (Order, Piece, Cut_Material, Section, Performance, 
                                ManpowerPlan, ProductionPlan, MaterialRequest)
# Register your models here.


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'work_order_number','order_slug', 'production_type', 'profile', 'order_colour', 
                    'order_finish', 'order_gauge', 'order_width', 'order_completed')
    list_display_links = ('id', 'order_slug')
    list_filter = ('profile', 'order_colour', 'order_finish', 'order_gauge', 'order_completed')
    # list_editable = ('is_published',)
    search_fields = ('id', 'order_slug', 'production_type', 'profile',)
    list_per_page = 25
admin.site.register(Order, OrdersAdmin)


class CutMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'coil_number', 'coil_gauge','coil_width', 'coil_colour', 
                    'coil_finish', 'coil_gauge', 'initial_mass', 'final_mass')
    list_display_links = ('id', 'coil_number')
    list_filter = ('order', 'coil_number', 'coil_gauge','coil_width', 'coil_colour', 
                    'coil_finish', 'coil_gauge')
    search_fields = ('id', 'order', 'coil_number')
    list_per_page = 25
admin.site.register(Cut_Material,CutMaterialAdmin)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'section_name')
    list_display_links = ('id', 'section_name')
    list_filter = ('id', 'section_name')
    search_fields = ('id', 'section_name')
    list_per_page =25

admin.site.register(Section, SectionAdmin)

class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("machine", "date", "shift", "machine_hourly_capacity", 
                    "shift_hours", "total_capacity","total_production", "percentage")
    list_display_links = ("machine", "date")
    list_filter = ("machine", "date", "shift", "shift_hours")
    search_fields = ("machine", "shift")
    list_per_page = 25

admin.site.register(Performance, PerformanceAdmin)

class PieceAdmin(admin.ModelAdmin):
    list_display = ("id","order", "coil", "piece_length", "prime_pieces", "reject_pieces",
        "reject_pieces", "total_running_meters", "total_tonage")
    list_display_links = ("piece_length",)
    list_filter = ("order", "coil", "piece_length")
    search_fields = ("order", "coil", "piece_length")
    list_per_page = 25
admin.site.register(Piece, PieceAdmin)


class ProductionPlanAdmin(admin.ModelAdmin):
    list_display = ("id","machine", "man_power", "date", "shift", "production_type",
        "colour", "order_number","gauge", "finish", "width")
    list_display_links = ("id",)
    list_filter = ("machine", "man_power", "date", "shift","production_type", "order_number")
    search_fields = ("machine", "man_power","shift","production_type", "order_number")
    list_per_page = 25
admin.site.register(ProductionPlan, ProductionPlanAdmin)


class ManpowerPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "machine", "date", "shift", "operator", "helpers")
    list_display_links = ("id",)
    list_filter = ("machine", "date", "shift", "operator")
    search_fields = ("machine", "date", "shift", "operator")
    list_per_page = 25
admin.site.register(ManpowerPlan, ManpowerPlanAdmin)

class MaterialRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "colour", "finish", "gauge", "width", "tonage")
    list_display_links = ("id",)
    list_filter = ("colour", "finish", "gauge", "width",)
    search_fields = ("colour", "finish", "gauge", "width",)
    list_per_page = 25
admin.site.register(MaterialRequest, MaterialRequestAdmin)