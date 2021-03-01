from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save
from frontend_choices import (PRODUCTION_TYPE_CHOICES, PROFILE_CHOICES, ORDER_COLOUR_CHOICES, 
                        ORDER_FINISH_CHOICES, PRODUCTION_BOND_CHOICES, ORDER_GAUGE_CHOICES,
                        ORDER_WIDTH_CHOICES, PIECE_STATUS_CHOICES, PRODUCTION_SHIFT_CHOICES)
from frontend_choices import ORDER_GAUGE_CHOICES
from django.utils.text import  slugify
from maintenance.models import Machine

# Create your models here.
class Order(models.Model):

    order_slug = models.SlugField(unique=True, blank=True)
    machine = models.ForeignKey(Machine, blank=True,on_delete=models.DO_NOTHING)
    production_type = models.CharField(choices=PRODUCTION_TYPE_CHOICES, max_length=30)
    production_bond = models.CharField(choices=PRODUCTION_BOND_CHOICES, max_length=50)
    profile = models.CharField(choices=PROFILE_CHOICES, max_length=50)
    order_number = models.CharField(max_length=50)
    work_order_number = models.CharField(max_length=50)
    order_colour = models.CharField(choices=ORDER_COLOUR_CHOICES, max_length=50)
    order_finish = models.CharField(choices=ORDER_FINISH_CHOICES, max_length=10)
    order_gauge  = models.IntegerField(choices=ORDER_GAUGE_CHOICES)
    order_width   = models.IntegerField()
    order_completed = models.BooleanField(default=False)
    order_tonage = models.DecimalField(max_digits=6,decimal_places=3,default=0)
    date_received = models.DateTimeField(default=datetime.now)
    shift = models.CharField(max_length=50)
    shift_date = models.DateField(default=datetime.now)

    class Meta: 
        ordering = ["date_received", "-profile"]

    def __str__(self):
        return (str(self.order_slug))

class Cut_Material(models.Model):
    order =  models.ForeignKey(Order, on_delete= models.CASCADE)
    coil_number = models.CharField(max_length=50)
    coil_gauge = models.IntegerField()
    coil_width = models.IntegerField()
    coil_colour = models.CharField(max_length=50)
    coil_finish = models.CharField(max_length=10)
    initial_mass = models.IntegerField()
    final_mass = models.IntegerField()
    new_or_used = models.BooleanField(default=True)
    date_received = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return (self.coil_number)

    
class Piece(models.Model):
    
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    coil = models.ForeignKey(Cut_Material ,on_delete=models.CASCADE)
    
    piece_length = models.DecimalField(max_digits=4, decimal_places=2)
    prime_pieces = models.IntegerField()
    reject_pieces = models.IntegerField()

    coil_constant = models.IntegerField(blank=True)
    prime_running_meters = models.DecimalField(max_digits=9, decimal_places=3)
    rejects_running_meters = models.DecimalField(max_digits=9, decimal_places=3)
    total_running_meters = models.DecimalField(max_digits=9, decimal_places=3)
    prime_tonage = models.DecimalField(max_digits=9, decimal_places=3)
    rejects_tonage = models.DecimalField(max_digits=9, decimal_places=3)
    total_tonage = models.DecimalField(max_digits=9, decimal_places=3)

    status = models.CharField(max_length=50,choices=PIECE_STATUS_CHOICES)
    transferred_pieces = models.IntegerField()

 
    def __str__(self):
        return (str(self.piece_length))

    class Meta:
        ordering = ["-order","piece_length"]

class StandardMaterial(models.Model):
    profile = models.CharField(max_length=50,choices=PROFILE_CHOICES)
    gauge = models.IntegerField(choices=ORDER_GAUGE_CHOICES)
    width = models.IntegerField(choices=ORDER_WIDTH_CHOICES)
    colour = models.CharField(max_length=50,choices=ORDER_COLOUR_CHOICES)
    finish = models.CharField(max_length=50,choices=ORDER_FINISH_CHOICES)
    total_production = models.IntegerField()
    on_floor_quantity = models.IntegerField()
    transferred_quantity = models.IntegerField()
    shipped_quantity = models.IntegerField()
    date = models.DateTimeField(default=datetime.now())


class Performance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    date = models.DateField()
    shift = models.CharField(max_length=50)
    machine_hourly_capacity = models.DecimalField(max_digits=6, decimal_places=3)
    shift_hours = models.DecimalField(decimal_places=2, max_digits=4)
    total_capacity = models.DecimalField(max_digits=6, decimal_places=3)
    total_production = models.DecimalField(max_digits=6, decimal_places=3)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        ordering = ['date', 'shift', 'machine']

    def __str__(self):
        return (self.machine.machine_name + str(self.machine.machine_number))

class Section(models.Model):
    section_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return (self.section_name)


'''
    For more details, check https://www.youtube.com/watch?v=hY5F3EGcff4
    We want to have a slug that is controlled unlike the code above

'''
def unique_slug_generator(model_instance, order_number, slug_field):
    
    order_slug = slugify(order_number)
    model_class = model_instance.__class__
    # check if the slug exists
    while model_class._default_manager.filter(order_slug=order_slug).exists():
        object_pk = model_class._default_manager.latest('pk')
        object_pk = object_pk.pk + 1

        order_slug = f'{order_slug}-{object_pk}'
    return order_slug 

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.order_slug:
        instance.order_slug = unique_slug_generator(instance, instance.order_number, instance.order_slug)

pre_save.connect(pre_save_post_receiver,sender=Order)

class ManpowerPlan(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    date = models.DateField()
    shift = models.CharField(max_length=50, choices=PRODUCTION_SHIFT_CHOICES)
    operator = models.CharField(max_length=50)
    helpers = models.IntegerField()
    
    def __str__(self):
        return (self.machine.machine_name +" " + str(self.machine.machine_number) +" " +
                self.shift)

class ProductionPlan(models.Model):
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    man_power = models.ForeignKey(ManpowerPlan, on_delete=models.CASCADE)
    date = models.DateField()
    shift = models.CharField(max_length=50, choices=PRODUCTION_SHIFT_CHOICES)
    production_type = models.CharField(max_length=50,choices=PRODUCTION_TYPE_CHOICES)
    order_number = models.CharField(max_length=50)
    colour = models.CharField(max_length=50, choices=ORDER_COLOUR_CHOICES)
    finish = models.CharField(max_length=50, choices=ORDER_FINISH_CHOICES)
    gauge = models.IntegerField(choices=ORDER_GAUGE_CHOICES)
    width = models.IntegerField(choices=ORDER_WIDTH_CHOICES)
    tonage = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return (self.shift)

class MaterialRequest(models.Model):

    date = models.DateField()
    colour = models.CharField(max_length=50, choices=ORDER_COLOUR_CHOICES)
    finish = models.CharField(max_length=50, choices=ORDER_FINISH_CHOICES)
    gauge = models.IntegerField(choices=ORDER_GAUGE_CHOICES)
    width = models.IntegerField(choices=ORDER_WIDTH_CHOICES)
    tonage = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return (str(self.date) + " " + self.colour + " " + self.finish)