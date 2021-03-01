from django.db import models
from frontend_choices import (PRODUCTION_TYPE_CHOICES, PROFILE_CHOICES, ORDER_COLOUR_CHOICES, 
                        ORDER_FINISH_CHOICES, PRODUCTION_BOND_CHOICES, ORDER_WIDTH_CHOICES,
                        COIL_LOCATION, COIL_STATUS)
from frontend_choices import ORDER_GAUGE_CHOICES
from datetime import datetime

# Create your models here.
class Coil(models.Model):
    coil_number = models.CharField(max_length=50)
    coil_gauge = models.IntegerField(choices=ORDER_GAUGE_CHOICES)
    coil_width = models.IntegerField(choices=ORDER_WIDTH_CHOICES)
    coil_colour = models.CharField(max_length=50, choices=ORDER_COLOUR_CHOICES)
    coil_finish = models.CharField(max_length=50, choices=ORDER_FINISH_CHOICES)
    initial_mass = models.IntegerField()
    final_mass = models.IntegerField()
    initial_running_meters = models.IntegerField()
    date_received = models.DateTimeField(default = datetime.now())
    location = models.CharField(max_length=50, choices=COIL_LOCATION, default="not assigned")
    production_transfer_date = models.DateTimeField(default=datetime.now())
    coil_status = models.CharField(max_length=50, choices=COIL_STATUS, default="undefined")

    def __str__(self):
        return (self.coil_number)

class Inventory(models.Model):
    date = models.DateTimeField()
    colour = models.CharField(max_length=50, choices=ORDER_COLOUR_CHOICES)
    finish = models.CharField(max_length=50, choices=ORDER_FINISH_CHOICES)
    gauge = models.IntegerField(choices=ORDER_GAUGE_CHOICES)
    width = models.IntegerField(choices=ORDER_WIDTH_CHOICES)
    bond_inventory = models.IntegerField()
    transferred = models.IntegerField()
    production_stock = models.IntegerField()

    def __str__(self):
        return (self.colour +" "+ self.finish)
