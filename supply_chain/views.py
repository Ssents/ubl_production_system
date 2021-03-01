from django.shortcuts import render, redirect
from supply_chain.models import Coil, Inventory
from frontend_choices import (ORDER_GAUGE_CHOICES, ORDER_COLOUR_CHOICES, 
                                ORDER_FINISH_CHOICES, ORDER_WIDTH_CHOICES)
from django.http import HttpResponse
from django.contrib import messages

from django.db.models import ExpressionWrapper
from django.db.models import (Count, F, Value, Sum, FloatField, Min, Max, Avg, 
                                IntegerField, Q)
from django.db.models.functions import Coalesce
import datetime



# Create your views here.

def main_dashboard(request):
    # inventory_report = Inventory.objects.filter(date__date = datetime.datetime.now().date())

    context = {
                'inventory_report':material_report(),
            }

    return render(request, 'supply_chain/main_dashboard.html', context)

def material_list_view(request):
    coils = Coil.objects.filter(location="Bond").order_by('coil_gauge','coil_width', 
                                                            'coil_colour','coil_finish', 
                                                        )
    context = {
        'gauge_choices': ORDER_GAUGE_CHOICES,
        'width_choices': ORDER_WIDTH_CHOICES,
        'colour_choices': ORDER_COLOUR_CHOICES,
        'finish_choices': ORDER_FINISH_CHOICES,
        'coils':coils,
    }
    return render(request,'supply_chain/material_list.html', context)

def create_coil(request):
    if request.method == "POST":
        coil_number = request.POST['coil_number']
        coil_gauge = request.POST['coil_gauge']
        coil_width = request.POST['coil_width']
        coil_colour = request.POST['coil_colour']
        coil_finish = request.POST['coil_finish']
        initial_mass = request.POST['initial_mass']
        initial_running_meters = request.POST['initial_running_meters']

        final_mass = initial_mass
        location = "Bond"
        coil_status = "New"

        coil = Coil.objects.create(coil_number=coil_number, coil_gauge=coil_gauge,
                                    coil_colour=coil_colour, coil_finish=coil_finish,
                                    coil_width=coil_width, initial_mass=initial_mass,
                                    final_mass=final_mass, 
                                    initial_running_meters=initial_running_meters,
                                    location=location, coil_status=coil_status
                                    )


        coil_created_message = "Coil " + coil_number + " has been created successfully"
        messages.add_message(request, messages.INFO, coil_created_message)

        return redirect('supply_chain:dashboard')

def edit_coil(request):
    if request.method == "POST":
        coil_id = request.POST['coil_id']
        coil = Coil.objects.get(pk=coil_id)
        coil_number = request.POST['coil_number']
        coil_gauge = request.POST['coil_gauge']
        coil_width = request.POST['coil_width']
        coil_colour = request.POST['coil_colour']
        coil_finish = request.POST['coil_finish']
        initial_mass = request.POST['initial_mass']
        initial_running_meters = request.POST['initial_running_meters']

        location = "Bond"
        coil_status = "New"

        coil.coil_number = coil_number
        coil.coil_gauge = coil_gauge
        coil.coil_width = coil_width
        coil.coil_gauge = coil_gauge
        coil.coil_colour = coil_colour
        coil.coil_finish = coil_finish
        coil.initial_mass = initial_mass
        coil.final_mass = initial_mass
        coil.initial_running_meters = initial_running_meters
        coil.location = location
        coil.coil_status = coil_status

        coil.save()

        coil_edited_message = "Coil " + coil_number + " has been edited successfully"
        messages.add_message(request, messages.INFO, coil_edited_message)

        return redirect('supply_chain:dashboard')
    else:
        return HttpResponse("Failed to save the form")

def get_coil_details(request, gauge, colour, finish, width, location):

    coils = Coil.objects.filter(location=location,
                                coil_colour=colour, coil_finish=finish,
                                coil_gauge=gauge, coil_width=width, final_mass__gt=0)

    context = {'gauge_choices': ORDER_GAUGE_CHOICES,
                'width_choices': ORDER_WIDTH_CHOICES,
                'colour_choices': ORDER_COLOUR_CHOICES,
                'finish_choices': ORDER_FINISH_CHOICES,
                'coils':coils,}

    return render(request,'supply_chain/dashboard.html', context)
    

def delete_coil(request):
    if request.method=="POST":
        coil_id = request.POST["coil_id"]
        coil = Coil.objects.get(pk=coil_id)
        coil.delete()


        coil_edited_message = "Coil " + coil.coil_number + " has been deleted successfully"
        messages.add_message(request, messages.INFO, coil_edited_message)
        

        return redirect('supply_chain:dashboard')

def transfer_coil(request):
    if request.method=="POST":
        coil_id = request.POST["coil_id"]
        coil = Coil.objects.get(pk=coil_id)
        coil.location = "Production"
        coil.production_transfer_date = datetime.datetime.now()
        coil.save()

        coil_edited_message = "Coil " + coil.coil_number + " has been transferred successfully"
        messages.add_message(request, messages.INFO, coil_edited_message)

        return redirect('supply_chain:dashboard')



def material_report():
    bond = Coil.objects.filter(location="Bond")
    production = Coil.objects.filter(location="Production")
    report = bond|production

    inventory_report = report.values('coil_gauge','coil_width', 'coil_colour', 
                                'coil_finish').order_by().annotate(
                production =Coalesce(Sum('final_mass', filter=Q(location="Production")),0),
                bond =Coalesce( Sum('initial_mass', filter=Q(location="Bond")),0),
                total =Coalesce( Sum('final_mass'),0),
                transferred =Coalesce(Sum('initial_mass', filter=Q(location="Production",
                    production_transfer_date__date=datetime.datetime.now().date())),0)
                )
    return inventory_report
    
    
