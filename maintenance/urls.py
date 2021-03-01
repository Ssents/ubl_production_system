from django.urls import path
from maintenance import views

urlpatterns = [
    path('', views.machines, name="machines"),
    path('<int:machine_id>', views.machine, name='dashboard'),
]