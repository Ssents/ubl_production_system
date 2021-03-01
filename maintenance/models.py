from django.db import models
from .choices import PRODUCTION_SECTION_CHOICES
# Create your models here.
class Machine(models.Model):
    machine_name = models.CharField(max_length=50)
    machine_number = models.CharField(max_length=50)
    machine_serial_number = models.CharField(max_length=50)
    machine_photo = models.ImageField(upload_to='photos/maintenance/machines/%Y/%m/%d/')
    machine_hourly_capacity = models.DecimalField(decimal_places=3, max_digits=6)

    section = models.CharField(
        max_length=50,
        choices= PRODUCTION_SECTION_CHOICES,
        default='ROOFING',
    )
    def __str__(self):
        return (self.machine_name + "-" + self.machine_number)

    class Meta:
        ordering = ["-section", "-machine_name", "-machine_serial_number"]