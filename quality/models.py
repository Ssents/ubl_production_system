from django.db import models
from maintenance.models import Machine
from production.models import Cut_Material
from frontend_choices import (PRODUCTION_TYPE_CHOICES, PROFILE_CHOICES, ORDER_COLOUR_CHOICES, 
                        ORDER_FINISH_CHOICES, PRODUCTION_BOND_CHOICES, COIL_TYPES_CHOICES,
                        ORDER_GAUGE_CHOICES, ORDER_WIDTH_CHOICES)
import datetime

# Create your models here.
class Profile_machines_matching(models.Model):
    profile = models.CharField(max_length=50, 
                                choices=PROFILE_CHOICES)
    producing_machine  = models.ForeignKey(Machine, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['producing_machine']
    
    def __str__(self):
        return self.profile


class Coil_parameters(models.Model):
    coil_type = models.CharField(max_length=50, choices=COIL_TYPES_CHOICES)
    coil_finish = models.CharField(max_length=50, choices=ORDER_FINISH_CHOICES)
    coil_gauge = models.IntegerField()
    coil_thickness = models.DecimalField(decimal_places=2, max_digits=4)
    coil_width = models.IntegerField()
    coil_constant = models.IntegerField()
    
    class Meta:
        ordering = ['coil_type', 'coil_gauge', 'coil_finish']
    
    def __str__(self):
        return self.coil_type

class Coil_description(models.Model):
    coil_type = models.CharField(max_length=50, choices=COIL_TYPES_CHOICES)
    coil_colour = models.CharField(max_length=50, choices=ORDER_COLOUR_CHOICES)
    coil_finish = models.CharField(max_length=50, choices=ORDER_FINISH_CHOICES)
    
    def __str__(self):
        return (self.coil_colour + self.coil_finish)

class Reconsiliation(models.Model):
    coil_number = models.CharField(max_length=50)
    coil_gauge = models.IntegerField()
    coil_width = models.IntegerField()
    coil_colour = models.CharField(max_length=50)
    coil_finish = models.CharField(max_length=50)
    initial_mass = models.IntegerField()
    final_mass = models.IntegerField()
    produced_mass = models.IntegerField()
    initial_running_meters = models.IntegerField()
    produced_running_meters = models.IntegerField()
    mass_gain = models.IntegerField()
    running_meters_gain = models.IntegerField()

    def __str__(self):
        return (self.coil_number) 

class StandardMaterialParameters(models.Model):
    profile = models.CharField(max_length=50,choices=PROFILE_CHOICES)
    gauge = models.IntegerField(choices=ORDER_GAUGE_CHOICES)
    has_standard_width = models.BooleanField(default=False)
    standard_width = models.IntegerField(choices=ORDER_WIDTH_CHOICES)
    has_standard_length = models.BooleanField(default=False)
    standard_length = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)