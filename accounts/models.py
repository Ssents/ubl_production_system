from django.db import models

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    hire_date = models.DateField()
    photo = models.ImageField(upload_to='photos/accounts/employee/%Y/%m/%d/', blank=True)
    department = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    employee_code = models.CharField(max_length=50)
    is_active = models.BooleanField()
    contact = models.CharField(max_length=14)
    email = models.EmailField()

    def __Str__(self):
        return (self.first_name)

    class Meta:
        ordering = ["-first_name", "-section", "job_title"]