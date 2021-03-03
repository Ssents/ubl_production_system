from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse

from maintenance.views import machine, shift_func
from maintenance.models import Machine
from production.models import (Order, Piece, Cut_Material, Performance, MaterialRequest, 
                                ProductionPlan, ManpowerPlan, MaterialRequest)
from quality.models import Coil_parameters, Coil_description, Reconsiliation, Profile_machines_matching
from supply_chain.models import Coil
from supply_chain.views import material_report


from django.db.models.functions import Coalesce
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView,
                                    DeleteView)
from django.contrib import messages
from django.core import serializers
from django.urls import reverse_lazy
import json
from django.db.models import (Count, F, Q, Value, Sum, FloatField, Min, Max, 
                                Avg, IntegerField, ExpressionWrapper, DateField)

from  frontend_choices import ( ORDER_COLOUR_CHOICES, PROFILE_CHOICES, ORDER_FINISH_CHOICES,
                                ORDER_GAUGE_CHOICES, ORDER_WIDTH_CHOICES, PRODUCTION_BOND_CHOICES,
                                PRODUCTION_TYPE_CHOICES, PRODUCTION_SHIFT_CHOICES,
                                DAYS_LIST_CHOICES, MONTH_LIST_CHOICES)

from .forms import OrderForm, PieceForm, ManpowerPlanForm
from .decorators import allowed_users

from itertools import chain
import datetime
import pandas as pd
import calendar



# Create your views here. 
@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def create_order_page(request, machine_id):
    machinery = get_object_or_404(Machine, pk=machine_id)
    profile = Profile_machines_matching.objects.filter(machine=machinery)
    context = {
                'machinery': machinery, 
                'profiles': profile,
                'colours':ORDER_COLOUR_CHOICES,
                'finish': ORDER_FINISH_CHOICES,
                'bond':PRODUCTION_BOND_CHOICES,
                'production_type':PRODUCTION_TYPE_CHOICES,
                'gauge':ORDER_GAUGE_CHOICES,
                'width':ORDER_WIDTH_CHOICES,
                }
    return render(request, 'production/order_form.html', context) 

@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def machine_dashboard(request):

    return render(request, 'production/dashboard.html')
    
@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def dashboard_search(request):
    if request.method == "POST":
        order_number = request.POST['order_number']
        colour = request.POST['order_colour']
    
    return render(request, 'production/dashboard.html')


@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def create_order(request, machine_id):
    machines = Machine.objects.get(pk=machine_id)
    
    if request.method=="POST": 
        production_type = request.POST['production_type']
        production_bond = request.POST['production_bond']
        profile = request.POST['profile']

        order_number = request.POST['order_number']
        work_order_number = request.POST['work_order_number']
        order_colour = request.POST['order_colour']
        order_finish = request.POST['order_finish']
        order_gauge  = request.POST['order_gauge']
        order_width   = request.POST['order_width']

        order_completed   = request.POST['order_completed']
        if order_completed==True:
            order_completed = True
        else:
            order_completed=False

        order_tonage = 0
        
        time_now = datetime.datetime.now().time()
        today = datetime.datetime.now()

        if time_now > datetime.time(8,0,0,0) and time_now < datetime.time(17, 30, 0, 0):
            shift = "Day"
            shift_date = today.date()
        elif time_now > datetime.time(0,0,0,0) and time_now < datetime.time(8,0,0,0):
            shift_date = datetime.datetime(today.year, today.month, today.day-1).date()
            shift = "Night"
        else:
            shift = "Night"
            shift_date = today.date()

        order = Order(machine=machines ,production_type=production_type, production_bond=production_bond,
            profile=profile, order_number=order_number, order_colour=order_colour, 
            order_finish=order_finish, order_gauge=order_gauge, order_width=order_width,
            shift=shift, shift_date=shift_date,order_tonage=order_tonage, 
            work_order_number=work_order_number,order_completed=order_completed)
        
        order.save()
        
        material = Cut_Material.objects.filter(order=order).values()
        material_list = Coil.objects.filter(coil_colour= order.order_colour,
                                            coil_finish=order.order_finish,
                                            coil_gauge=order.order_gauge,
                                            coil_width=order.order_width,
                                            final_mass__gt =0,
                                            location="Production")

        context = {
                    "order_id": order.id,
                    "order_number": order.order_number,
                    "order_gauge": order.order_gauge,
                    "order_colour": order.order_colour,
                    "order_width": order.order_width,
                    "order_finish": order.order_finish,
                    "material": material,
                    "material_list": material_list,
                    "machine": order.machine,

                }
        return render(request, 'production/material_page.html', context)




@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def edit_order_page(request, order_id):
    order = Order.objects.get(pk=order_id)

    context = {
                "order": order, 
                "machine": order.machine,
                "order_id": order_id,
                "order_production_type": order.production_type,
                "order_production_bond": order.production_bond,
                "order_profile": order.profile,
                "order_number":order.order_number,
                "order_colour": order.order_colour,
                "order_finish": order.order_finish,
                "order_gauge": order.order_gauge,
                "order_width": order.order_width,
                'profile':PROFILE_CHOICES,
                'colours':ORDER_COLOUR_CHOICES,
                'finish': ORDER_FINISH_CHOICES,
                'bond':PRODUCTION_BOND_CHOICES,
                'production_type':PRODUCTION_TYPE_CHOICES,
                'gauge':ORDER_GAUGE_CHOICES,
                'width':ORDER_WIDTH_CHOICES,
            }

    return render(request, 'production/edit_order.html', context)

@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def edit_order(request):
    if request.method =="POST":
        order_id = request.POST['order_id']
        order = Order.objects.get(pk=order_id)
        machine = order.machine
        machine_id = machine.id

        production_type = request.POST['production_type']
        production_bond = request.POST['production_bond']
        profile = request.POST['profile']
        order_number = request.POST['order_number']
        order_colour = request.POST['order_colour']
        order_finish = request.POST['order_finish']
        order_gauge  = request.POST['order_gauge']
        order_width   = request.POST['order_width']
        work_order_number = request.POST['work_order_number']
        order_complete = request.POST['order_completed']

        # editing the order
        order.production_type = production_type
        order.production_bond = production_bond
        order.profile = profile
        order.order_number = order_number
        order.order_colour = order_colour
        order.order_finish = order_finish
        order.order_gauge = order_gauge
        order.order_width = order_width
        order.work_order_number = work_order_number
        order.order_completed = order_complete

        order.save()

        # editing the material
        materials = Cut_Material.objects.filter(order=order)
        for material in materials:
            material.coil_colour = order_colour
            material.coil_finish = order_finish
            material.coil_gauge = order_gauge
            material.coil_width = order_width
            material.save()   

    return redirect("maintenance:dashboard", machine_id = machine_id)

@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def delete_order(request, order_id):
    order = get_object_or_404(Order,pk=order_id)
    machine = order.machine
    machine_id = machine.id
    order.delete()
    material_list = Cut_Material.objects.filter(order=order)
    for material in material_list:
        update_coil_mass(material)
    
    return redirect("maintenance:dashboard", machine_id = machine_id)

   
@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def create_coil(request, machine_id, order_id):
    machine = Machine.objects.get(pk=machine_id)
    order = Order.objects.get(pk=order_id)

    if request.method=="POST":
        coil_number = request.POST['coil-number']
        coil_gauge = order.order_gauge
        coil_width = order.order_width
        coil_colour = order.order_colour
        coil_finish = order.order_finish
        initial_mass = request.POST['initial-mass']
        final_mass = request.POST['final-mass']

        material = Cut_Material(order=order, coil_number=coil_number, coil_gauge=coil_gauge,
                    coil_width=coil_width, coil_colour=coil_colour, initial_mass=initial_mass, 
                    coil_finish=coil_finish,final_mass=final_mass)
        material.save()
        context = {
                    
                    "machine_id": machine_id,
                    "order_id": order_id,
                    "coil_id": material.id,
                    "coil_number": material.coil_number,
                    "coil_gauge": material.coil_gauge,
                    "coil_colour": material.coil_colour,
                    "coil_width": material.coil_width,
                    "coil_finish": material.coil_finish,
                    "initial_mass": material.initial_mass,
                    "final_mass": material.final_mass,
        }
        return render(request, 'production/pieces_form.html', context)

@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def edit_material_page(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    machine = order.machine
    machine_id = machine.id
    material = Cut_Material.objects.filter(order=order).values()

    material = Cut_Material.objects.filter(order=order).values()
    material_list = Coil.objects.filter(coil_colour= order.order_colour,
                                            coil_finish=order.order_finish,
                                            coil_gauge=order.order_gauge,
                                            coil_width=order.order_width,
                                            final_mass__gt =0,
                                            location="Production")


    if material is not None:
        context = {
                    'order':order,
                    'machine_id': machine_id,
                    'order_id': order_id,
                    'material':material,
                    'message': 'Material Avaiable',
                    "material_list": material_list,
                    "machine":machine                  
                    }
        return render(request, 'production/material_page.html', context)
    else:
        context = {
            'message':'Material is not in the system, please add'
        }
        return render(request, 'production/material_page.html', context)

@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def edit_material(request):
    if request.method == 'POST':
        coil_id = request.POST['coil_id']
        material = Cut_Material.objects.get(pk=coil_id)
        
        coil_number = request.POST['coil_number']
        initial_mass: request.POST['initial_mass']
        final_mass: request.POST['final_mass']

        material.coil_number = coil_number
        material.initial_mass = initial_mass
        material.final_mass = final_mass
        material.save()
        create_reconsiliation(material_number = material.coil_number, 
                            material_gauge = material.coil_gauge, 
                            material_width = material.coil_width,
                            material_colour = material.coil_colour, 
                            material_finish = material.coil_finish)  
        order = material.order
        machine = order.machine
        machine_id = machine.id

        return redirect("maintenance:dashboard", machine_id = machine_id)

@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def create_material_ajax(request):
    order_id = request.GET.get('order_id', None)
    order = Order.objects.get(pk=order_id)
    machine = order.machine
    machine_id = machine.id
    
    # order = get_object_or_404(Order, pk=order_id)
    coil_number = request.GET.get('coil_number', None)
    initial_mass = request.GET.get('initial_mass', None)
    final_mass = request.GET.get('final_mass', None)
    
    coil_gauge = order.order_gauge
    coil_width = order.order_width
    coil_colour = order.order_colour
    coil_finish = order.order_finish

    material = Cut_Material.objects.create(order=order, coil_number=coil_number, coil_gauge=coil_gauge,
                coil_width=coil_width, coil_colour=coil_colour, initial_mass=initial_mass, 
                coil_finish=coil_finish,final_mass=final_mass)

    supply_chain_coil = Coil.objects.get(coil_number=coil_number, 
                                            coil_gauge=material.coil_gauge,
                                            coil_colour=material.coil_colour,
                                            coil_finish=material.coil_finish, 
                                            coil_width=material.coil_width)

    supply_chain_coil.final_mass = final_mass
    supply_chain_coil.save()

    update_coil_mass(material)
    # create_reconsiliation(coil_number, material.coil_gauge, material.coil_width,
    #                         material.coil_colour, material.coil_finish)

    material_data = {
                        'material_id': material.id,
                        'coil_number': material.coil_number,
                        'initial_mass': material.initial_mass,
                        'final_mass': material.final_mass,
                        'order_id': order_id,
                        'machine_id': machine_id,
                        }

    data = {'material_data':material_data, 'error':'success'}
    return JsonResponse(data)
    
@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def edit_material_ajax(request):
    material_id = request.GET.get('coil_id')
    material = Cut_Material.objects.get(pk=material_id)
    coil_number = request.GET.get('coil_number')
    initial_mass = request.GET.get('initial_mass')
    final_mass = request.GET.get('final_mass')

    material.coil_number = coil_number
    material.initial_mass = initial_mass
    material.final_mass = final_mass

    material.save()

    update_coil_mass(material)

    supply_chain_coil = Coil.objects.get(coil_number=coil_number, 
                                            coil_gauge=material.coil_gauge,
                                            coil_colour=material.coil_colour,
                                            coil_finish=material.coil_finish, 
                                            coil_width= material.coil_width)

    supply_chain_coil.final_mass = final_mass
    supply_chain_coil.save()
    create_reconsiliation(material_number = material.coil_number, 
                        material_gauge = material.coil_gauge, 
                        material_width = material.coil_width,
                        material_colour = material.coil_colour, 
                        material_finish = material.coil_finish)   

    material_data = {
                        'material_id': material.id,
                        'coil_number': material.coil_number,
                        'initial_mass': material.initial_mass,
                        'final_mass': material.final_mass,
                    }
    data = {'material_data':material_data, 'message':'success'}
    return JsonResponse(data)


@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def delete_material_ajax(request):
    material_id = request.GET.get('material_id')
    material = Cut_Material.objects.get(pk=material_id)

    data = {'deleted':'', 'message':''}
    
    if material:
        order = material.order
        coil_number = material.coil_number
        coil_gauge = material.coil_gauge
        coil_width = material.coil_width
        coil_colour = material.coil_colour
        coil_finish = material.coil_finish

        material.delete()

        update_coil_mass(material)
        create_order_tonage(order)
        create_reconsiliation(material_number = material.coil_number, 
                    material_gauge = material.coil_gauge, 
                    material_width = material.coil_width,
                    material_colour = material.coil_colour, 
                    material_finish = material.coil_finish)  
        
        data['deleted'] = True
        data['message'] = str(material.coil_number) + ' successfully deleted'
        # update_coil_mass(material)
        return JsonResponse(data)
    else:
        data['deleted'] = False
        data['message'] = 'material id does not exist' 

    return JsonResponse(data)
    


    

# PIECES
# list pieces
@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def pieces_template(request, machine_id, order_id, coil_id):
    order =Order.objects.get(pk=order_id)
    coil = Cut_Material.objects.get(pk=coil_id)
    pieces = Piece.objects.filter(order=order, coil=coil).values()
    coil_id_number= coil_id
    machine_id_number = machine_id
    order_id_number = order_id
    context = {
                'coil_id':coil_id_number,
                'order_id':order_id_number,
                'machine_id':machine_id_number,
                'coil': coil,
                'machine': Machine.objects.get(pk=machine_id),
                'order': Order.objects.get(pk=order_id),
                'pieces': pieces
                }
    return render(request, 'production/pieces_form.html', context);

@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def create_pieces(request, coil_id, machine_id, order_id):
    order = Order.objects.get(pk=order_id)
    machine = Machine.objects.get(pk=machine_id)    
    coil = Cut_Material.objects.get(pk=coil_id)

    coil_number = coil.coil_number
    order_number = order.order_number

    piece_length = request.GET.get('piece_length', None)
    prime_pieces = request.GET.get('prime_pieces', None)
    rejects_pieces = request.GET.get('reject_pieces', None)

    # arithmetic on the coil
    # get the type of coil first
    coil_type = Coil_description.objects.get(coil_colour=order.order_colour,
                                            coil_finish=order.order_finish).coil_type
    coil_parameters = Coil_parameters.objects.get(coil_type=coil_type, 
                                                    coil_gauge=order.order_gauge,
                                                    coil_width=order.order_width,
                                                    coil_finish=order.order_finish)

    coil_constant = coil_parameters.coil_constant

    prime_running_meters = int(prime_pieces) * float(piece_length)
    rejects_running_meters = float(piece_length) * int(rejects_pieces)
    total_running_meters = prime_running_meters + rejects_running_meters

    prime_tonage = prime_running_meters/coil_constant
    rejects_tonage = rejects_running_meters/coil_constant
    total_tonage = prime_tonage + rejects_tonage

    
    obj = Piece.objects.create(order=order, coil=coil,piece_length=piece_length, 
                                prime_pieces=prime_pieces,reject_pieces=rejects_pieces,
                                coil_constant=coil_constant, 
                                prime_running_meters=prime_running_meters,
                                rejects_running_meters=rejects_running_meters,
                                total_running_meters= total_running_meters,
                                prime_tonage= prime_tonage, rejects_tonage=rejects_tonage,
                                total_tonage= total_tonage, 
                                status="Not Transferred",
                                transferred_pieces=0)

    create_reconsiliation(material_number = coil.coil_number, 
                            material_gauge = coil.coil_gauge, 
                            material_width = coil.coil_width,
                            material_colour = coil.coil_colour, 
                            material_finish = coil.coil_finish)

    create_order_tonage(order) 

    piece = {
            'id':obj.id,
            'order':order_number,
            'coil': coil_number,
            'piece_length':obj.piece_length,
            'prime_pieces':obj.prime_pieces,
            'reject_pieces':obj.reject_pieces,

            }
            
    data ={'piece': piece}
    return JsonResponse(data)

@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def update_piece(request):
    # get data from the form first
    piece_id = request.GET.get('piece_id', None)
    updated_piece_length = request.GET.get('updated_piece_length', None)
    updated_prime_pieces = request.GET.get('updated_prime_pieces', None)
    updated_reject_pieces = request.GET.get('updated_reject_pieces', None)

    # get coil and order number details
    order_id = request.GET.get('order_id', None)
    coil_id = request.GET.get('coil_id', None)
    order = Order.objects.get(pk=order_id)
    coil = Cut_Material.objects.get(pk=coil_id)

    #query for the object
    piece = Piece.objects.get(pk=piece_id)
    piece.piece_length = updated_piece_length
    piece.prime_pieces = updated_prime_pieces
    piece.reject_pieces = updated_reject_pieces


    coil_type = Coil_description.objects.get(coil_colour=order.order_colour,
                                            coil_finish=order.order_finish).coil_type
    coil_parameters = Coil_parameters.objects.get(coil_type=coil_type, 
                                                    coil_gauge=order.order_gauge,
                                                    coil_width=order.order_width,
                                                    coil_finish=order.order_finish)

    coil_constant = coil_parameters.coil_constant

    prime_running_meters = int(updated_prime_pieces) * float(updated_piece_length)
    rejects_running_meters = float(updated_piece_length) * int(updated_reject_pieces)
    total_running_meters = prime_running_meters + rejects_running_meters

    prime_tonage = prime_running_meters/coil_constant
    rejects_tonage = rejects_running_meters/coil_constant
    total_tonage = prime_tonage + rejects_tonage


    piece.prime_running_meters = prime_running_meters
    piece.rejects_running_meters = rejects_running_meters
    piece.total_running_meters = total_running_meters
    piece.prime_tonage = prime_tonage
    piece.rejects_tonage = rejects_tonage
    piece.total_tonage = total_tonage
    
    piece.save()
    create_order_tonage(order)
    create_reconsiliation(material_number=coil.coil_number, 
                           material_gauge= coil.coil_gauge, 
                           material_width = coil.coil_width,
                           material_colour= coil.coil_colour, 
                           material_finish= coil.coil_finish)

    piece = {
        'piece_id':piece.id,
        'order': order.order_number,
        'coil':  coil.coil_number,
        'piece_length':piece.piece_length,
        'prime_pieces':piece.prime_pieces,
        'reject_pieces':piece.reject_pieces
        }

    data = {'piece_data': piece, 'message':'success'}
    return JsonResponse(data)


@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def list_pieces(request, machine_id, order_id):
    order = Order.objects.get(pk=order_id)
    machine = Machine.objects.get(pk=machine_id)

    pieces = Piece.objects.filter(order=order)

    return JsonResponse(pieces, safe=False)

@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def  delete_piece(request):
    coil_id = request.GET.get('coil_id', None)
    coil_id = int(coil_id)
    piece = Piece.objects.get(pk=coil_id)
    material = piece.coil

    coil_number = material.coil_number
    coil_gauge = material.coil_gauge
    coil_width = material.coil_width
    coil_colour = material.coil_colour
    coil_finish = material.coil_finish

    order =piece.order
    piece.delete()
    
    create_reconsiliation(material_number = material.coil_number, 
                    material_gauge = material.coil_gauge, 
                    material_width = material.coil_width,
                    material_colour = material.coil_colour, 
                    material_finish = material.coil_finish)  
    create_order_tonage(order)
    data = {
        'deleted': True
        }
    return JsonResponse(data)

@login_required
@allowed_users(allowed_roles=['Operator', 'Admin', 'Supervisor'])
def material_page(request):
    order_id = request.GET.get('order_id', None)
    order = Order.objects.get(pk=order_id)
    order_id = order.id
    machine = order.machine
    machine_id = machine.id
    material = Cut_Material.objects.filter(order=order).values()
    context = {
                'material':material,
                'order_id': order_id,
                'machine_id':machine_id
    }    
    return render(request, 'production/material_page.html', context)

@login_required
@allowed_users(allowed_roles=['Operator', 'Supervisor'])
def running_meters(request):
    running_meters_data = Piece.objects.annotate(running_meters=ExpressionWrapper(
                            F('piece_length') * F('prime_pieces'),
                            output_field=FloatField())).values()
    rm_data =  Piece.objects.annotate(rm=ExpressionWrapper(
                                            F('piece_length') * F('prime_pieces'), 
                                            output_field=FloatField()
                                            )
                                    ).values()
    order = Order.objects.all()
    piece = Piece.objects.all()

    order_running_meters = order.values('order_colour', 'order_finish', 'order_gauge', 
        'order_width').order_by().annotate(running_meters=Sum(ExpressionWrapper(
                F('piece__piece_length')*F('piece__prime_pieces') + 
                F('piece__piece_length')*F('piece__reject_pieces')
                , output_field=FloatField()
                ))
            ).values('order_colour', 'order_finish','order_gauge','order_width', 'running_meters')

    context = {
                'running_meters': running_meters_data,
                'lover': 'shabaaa',
                'rm': rm_data,
                'order_running_meters': order_running_meters,
    }
    return render(request, 'production/running_meters.html', context)


##supervisor
@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def list_products(request):
    date = datetime.datetime.now().date()
    standard_list = Order.objects.filter(production_type__in=["Standard"], 
                                                shift_date=shift_func()['shift_date'])

    pieces =Piece.objects.filter(order__in=standard_list)
    report = pieces.values('order__profile','order__order_number','order__order_colour','order__order_finish',
                            'order__order_gauge','order__order_finish').order_by().annotate(pieces=
                                Sum('prime_pieces'), 
                                transferred_pieces_sum=Sum('transferred_pieces'),
                                not_transferred=ExpressionWrapper(
                                                Sum('prime_pieces')-
                                                Sum('transferred_pieces'),
                                                output_field=IntegerField()
                                                )
                                            ).values('order__profile','order__order_number',
                                        'order__order_colour', 'order__order_finish', 
                                        'order__order_gauge', 'order__order_finish',
                                        'pieces','transferred_pieces_sum','not_transferred')
    
    orders = Order.objects.filter(shift_date = datetime.datetime.now().date(),
                                    production_type="Work Order")


    context={
        "material_list": report,
        "production_date":datetime.datetime.now(),
        "orders_list": orders,
    }
    return render(request, 'production/standard_material_list.html', context)

def orders(request):
    return None

def finished_goods_search(request):
    if request.method == "POST":
        date = request.POST['production_date']
        pieces = Piece.objects.filter(order__shift_date=date, 
                                        order__production_type="Standard",
                                        prime_pieces__gt=0)
        orders = Order.objects.filter(shift_date=date, production_type="Work Order",
                                        )

        context = {
                        "standard_list": pieces,
                        "orders_list": orders,
                        "production_date": date,
                        "today": datetime.datetime.now().date(),
                    }
        return render(request, 'production/supervisor/material_search_list.html', context)


@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def list_production_details(request, profile,order_number, order_gauge, order_colour, order_finish):
    date = shift_func()['shift_date']
    order_list = Piece.objects.filter(order__order_number=order_number, order__order_gauge=order_gauge,
                                     order__order_colour=order_colour, order__order_finish=order_finish,
                                     order__profile=profile, order__shift_date=date)
    context = {
                "order_list": order_list,
            }
    return render(request, "production/standard_list_details.html", context)

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])            
def list_order(request, order_number):
    order_list = Order.obejcts.filter(order_number=order_number)
    context = {}
    if order:
        context = {'message' : 'Order_exists',
                    'order_list': order_list}
    else:
        context={'message':'Order does not exist'}
    
    return render(request, 'production/order_search_list.html', context)

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def transfer_material(request, piece_id):
    piece = Piece.objects.get(pk=piece_id)
    profile = piece.order.profile
    order_number = piece.order.order_number
    order_gauge = piece.order.order_gauge
    order_colour = piece.order.order_colour
    order_finish = piece.order.order_finish

    piece.status = "Transferred"
    piece.transferred_pieces = piece.prime_pieces
    piece.save()
    
    return redirect ('production:list-orders', profile, order_number, order_gauge, order_colour, order_finish)

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def reverse_transfer(request, piece_id):
    piece = Piece.objects.get(pk=piece_id)
    profile = piece.order.profile
    order_number = piece.order.order_number
    order_gauge = piece.order.order_gauge
    order_colour = piece.order.order_colour
    order_finish = piece.order.order_finish

    piece.status = "Not Transferred"
    piece.transferred_pieces = 0
    piece.save()
    
    return redirect ('production:list-orders', profile, order_number, order_gauge, order_colour, order_finish)

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def transfer_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    pieces = Piece.objects.filter(order=order)
    for piece in pieces:
        piece.status = "Transferred"
        piece.save()
    return redirect("production:list_products")
    

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def planer(request):
    machines = Machine.objects.all()
    plan = ProductionPlan.objects.filter(date__gte=datetime.datetime.now().date()).order_by(
        'date', 'shift', 'machine'
    )
    date = ProductionPlan.objects.filter(
                                            date__gte=datetime.datetime.now().date()
                                        ).values('date').distinct()
    context = {'inventory': material_report_planer()['report'],
                'colour': ORDER_COLOUR_CHOICES,
                'gauge': ORDER_GAUGE_CHOICES,
                'width': ORDER_WIDTH_CHOICES,
                'finish': ORDER_FINISH_CHOICES,
                'shifts': PRODUCTION_SHIFT_CHOICES,
                'dates':date,
                'machines': machines,
                'production_type': PRODUCTION_TYPE_CHOICES,
                'plan':plan,
    }
    return render(request, 'production/supervisor/planner.html', context)

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def create_plan(request):
    if request.method =="POST":

        machine_id = request.POST['machine_id']
        shift = request.POST['shift']
        production_type = request.POST['production_type']
        order_number = request.POST['order_number']

        gauge = request.POST['gauge']
        width = request.POST['width']
        colour = request.POST['colour']
        finish = request.POST['finish']
        
        tonage = request.POST['tonage']
        # tonage = float(int(tonage/1000)

        date = datetime.datetime.now().date()
        machine = Machine. objects.get(pk=machine_id)

        try:
            operator = ManpowerPlan.objects.get(date=date, shift=shift, machine=machine)
        except ManpowerPlan.DoesNotExist:
            operator_message = machine.machine_name +" "+machine.machine_number + " has not been allocated manpower to run for the " + shift + " shift." 
            messages.add_message(request, messages.INFO, operator_message)
            return redirect('production:planer')

        material_dict= material_request_create(colour, finish, int(gauge), 
                                                int(width), float(tonage))
        request_tonage = material_dict['material_request']
        bond_tonage = material_dict['bond_tonage']
        
        if bond_tonage < request_tonage:
            operator_message = "Material is not enough"
            messages.add_message(request, messages.INFO, operator_message)
            return redirect('production:planer')
        else:
            try:
                material_request = MaterialRequest.objects.get(colour=colour, 
                                                    finish=finish, gauge=gauge, 
                                                    width=width,
                                                    date=datetime.datetime.now().date())
                material_request.tonage = request_tonage
                material_request.save()
            except MaterialRequest.DoesNotExist:
                material_request = MaterialRequest.objects.create(colour=colour, 
                                            finish=finish, gauge=gauge, width=width,
                                            date=datetime.datetime.now().date(),
                                            tonage=request_tonage)

        plan = ProductionPlan.objects.create(
            machine = machine, man_power = operator, date=date, shift=shift,
            production_type=production_type, order_number = order_number,
            colour=colour, finish=finish, gauge=gauge, width=width,
            tonage=tonage
        )

        return redirect('production:planer')

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def delete_plan(request):
    if request.method=="POST":
        plan_id = request.POST['plan_id']
        plan = ProductionPlan.objects.get(pk=plan_id)
        plan.delete()

        material_dict= material_request_create(colour=plan.colour, finish=plan.finish, 
                                                    gauge=int(plan.gauge), 
                                                    width=int(plan.width), 
                                                    requested_tonage=0)

        request_tonage = material_dict['material_request']
        bond_tonage = material_dict['bond_tonage']
        
        if bond_tonage < request_tonage:
            operator_message = "Material is not enough"
            messages.add_message(request, messages.INFO, operator_message)
            return redirect('production:planer')
        else:
            try:
                material_request = MaterialRequest.objects.get(colour=plan.colour, 
                                                    finish=plan.finish, gauge=plan.gauge, 
                                                    width=plan.width,
                                                    date=datetime.datetime.now().date())
                material_request.tonage = request_tonage
                material_request.save()
            except MaterialRequest.DoesNotExist:
                material_request = MaterialRequest.objects.create(colour=plan.colour, 
                                            finish=plan.finish, gauge=plan.gauge, width=plan.width,
                                            date=datetime.datetime.now().date(),
                                            tonage=request_tonage)


    return redirect('production:planer')

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def edit_plan(request):
    if request.method =="POST":
        plan_id = request.POST['plan_id']
        machine_id = request.POST['machine_id']
        shift = request.POST['shift']
        production_type = request.POST['production_type']
        order_number = request.POST['order_number']
        tonage = request.POST['tonage']

        date = datetime.datetime.now().date()
        machine = Machine. objects.get(pk=machine_id)

        try:
            operator = ManpowerPlan.objects.get(date=date, shift=shift, machine=machine)
        except ManpowerPlan.DoesNotExist:
            operator_message = machine.machine_name +" "+machine.machine_number + " has not been allocated manpower to run for the " + shift + " shift." 
            messages.add_message(request, messages.INFO, operator_message)
            return redirect('production:planer')

        plan = ProductionPlan.objects.get(pk=plan_id)
        plan.machine = machine
        plan.production_type = production_type
        plan.shift = shift
        plan.order_number = order_number
        tonage_to_request = float(tonage) - float(plan.tonage)
        plan.tonage = tonage

        if tonage_to_request < 0:
            tonage_to_request = 0
        
        material_dict= material_request_create(colour=plan.colour, finish=plan.finish, 
                                                gauge=int(plan.gauge), 
                                                width=int(plan.width), 
                                                requested_tonage=tonage_to_request)
        request_tonage = material_dict['material_request']
        bond_tonage = material_dict['bond_tonage']
        
        if bond_tonage < request_tonage:
            operator_message = "Material is not enough"
            messages.add_message(request, messages.INFO, operator_message)
            return redirect('production:planer')
        else:
            try:
                material_request = MaterialRequest.objects.get(colour=plan.colour, 
                                                    finish=plan.finish, gauge=plan.gauge, 
                                                    width=plan.width,
                                                    date=datetime.datetime.now().date())
                material_request.tonage = request_tonage
                material_request.save()
            except MaterialRequest.DoesNotExist:
                material_request = MaterialRequest.objects.create(colour=plan.colour, 
                                            finish=plan.finish, gauge=plan.gauge, width=plan.width,
                                            date=datetime.datetime.now().date(),
                                            tonage=request_tonage)

        plan.save()
        plan_edited_message = "Plan edited successfully" 
        messages.add_message(request, messages.INFO, plan_edited_message)
        return redirect('production:planer')

def search_production_plan(request):
    if request.method == "POST":
        search_date = request.POST['date']
        machines = Machine.objects.all()
        production_plan = ProductionPlan.objects.filter(date=search_date)

        context = {
            'inventory': material_report_planer()['report'],
            'colour': ORDER_COLOUR_CHOICES,
            'gauge': ORDER_GAUGE_CHOICES,
            'width': ORDER_WIDTH_CHOICES,
            'finish': ORDER_FINISH_CHOICES,
            'shifts': PRODUCTION_SHIFT_CHOICES,
            'dates':search_date,
            'machines': machines,
            'production_type': PRODUCTION_TYPE_CHOICES,
            'plan':production_plan,
        }

        return render(request, 'production/supervisor/planner.html', context)

class ManpowerPlanListView(ListView):
    
    model = ManpowerPlan
    template_name = "production/supervisor/manpower_list.html"
    context_object_name = "manpower_list"

    def get_queryset(self):
        manpower_list = ManpowerPlan.objects.filter(date=datetime.datetime.now().date())
        return manpower_list
    
    def get_context_data(self, **kwargs):
        date = datetime.datetime.now().date()
        context = super().get_context_data(**kwargs)
        context['form'] = ManpowerPlanForm
        context['machines'] = Machine.objects.all()
        context['shifts'] = PRODUCTION_SHIFT_CHOICES
        context['date'] = date
        context['months'] = MONTH_LIST_CHOICES
        context['days'] = DAYS_LIST_CHOICES
        return context

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def manpower_create(request):
    if request.method =="POST":
        machine_id = int(request.POST['machine_id'])
        machine = Machine.objects.get(pk=machine_id)
        day = request.POST['day']
        month = request.POST['month']
        year = datetime.datetime.now().year
        date = datetime.datetime(year, int(month), int(day)).date()
        shift = request.POST['shift']
        operator = request.POST['operator']
        helpers = int(request.POST['helpers'])

        
        plan = ManpowerPlan.objects.filter(machine=machine,
                                        date=date, shift=shift)
        
        if plan:
            plan_edited_message = "Machine has been planed for" 
            messages.add_message(request, messages.INFO, plan_edited_message)
            return redirect('production:manpower_list')
        
        ManpowerPlan.objects.update_or_create(machine=machine, date=date, shift=shift, 
                                            operator=operator,
                                            helpers=helpers)

    return redirect('production:manpower_list')

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def manpower_edit(request):
    if request.method == "POST":
        plan_id = request.POST['plan_id']
        machine_id = request.POST['machine_id']
        shift = request.POST['shift']
        operator = request.POST['operator']
        helpers = request.POST['helpers']

        plan = ManpowerPlan.objects.get(pk=int(plan_id))
        machine = Machine.objects.get(pk=int(machine_id))
        plan.machine = machine
        plan.shift = shift
        plan.operator = operator
        plan.helpers = helpers

        check_plan = ManpowerPlan.objects.filter(machine=machine, shift=shift, date=plan.date)
        if check_plan:
            plan_edited_message = "Machine has been planed for" 
            messages.add_message(request, messages.INFO, plan_edited_message)
            return redirect('production:manpower_list')
        plan.save()

    return redirect('production:manpower_list')

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def manpower_delete(request):
    if request.method == "POST":
        plan_id = request.POST['plan_id']
        plan = ManpowerPlan.objects.get(pk=plan_id)
        plan.delete()

    return redirect('production:manpower_list')


@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
class ManpowerPlanCreateView(CreateView):
    model = ManpowerPlan
    template_name = "production/supervisor/manpower_create.html"
    fields = "__all__"  
    success_url = reverse_lazy('production:manpower_list')

def manpower_search_list(request):
    if request.method == "POST":
        date = request.POST['production_date']
        manpower_list = ManpowerPlan.objects.filter(date=date)

        context ={
            "manpower_list":manpower_list,
        }
        context['form'] = ManpowerPlanForm
        context['machines'] = Machine.objects.all()
        context['shifts'] = PRODUCTION_SHIFT_CHOICES
        context['date'] = date
        context['months'] = MONTH_LIST_CHOICES
        context['days'] = DAYS_LIST_CHOICES

        return render(request, "production/supervisor/manpower_list.html", context)




@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def material_request_list(request):
    date = datetime.datetime.now().date()
    material_list = MaterialRequest.objects.filter(date=date)
    coils = Coil.objects.filter(final_mass__gt=0)
    context = {
        "material_list":material_list,
        "coils": coils
    }
    return render(request,'production/supervisor/material_request_list.html', context)

def material_request_create(colour, finish, gauge, width, requested_tonage=0):
    date = datetime.datetime.now().date()
    # get all the planned material from today and onwards
    planned_material = float(ProductionPlan.objects.filter(gauge=gauge, width=width, 
                                            colour=colour, finish=finish,
                                            date__gte=date).values().aggregate(
                                                total = Coalesce( Sum('tonage'),0)
                                            )['total']) + float(requested_tonage)

    # get all the coil tonages at the bond and the production floor
    production_tonage = Coil.objects.filter(location="Production",final_mass__gt=0,
                                            coil_colour=colour, coil_finish=finish,
                                            coil_gauge=gauge, coil_width=width).aggregate(
                        total_tonage= Coalesce( Sum('final_mass'),0))['total_tonage']/1000
    bond_tonage = Coil.objects.filter(location="Bond", final_mass__gt=0,
                                    coil_colour=colour, coil_finish=finish,
                                    coil_gauge=gauge, coil_width=width).values().aggregate(
                        total_tonage= Coalesce( Sum('final_mass'),0))['total_tonage']/1000

    #  If material required is greater than that on the floor, then make check the bond
    material_required_from_bond = planned_material - production_tonage

    if material_required_from_bond <= 0:
        material_request_tonage = 0
    else:
        material_request_tonage = material_required_from_bond

    return {'material_request':material_request_tonage, 'bond_tonage':bond_tonage}

def material_list(request):
    material = Coil.objects.filter(location="Production", final_mass__gt=0)
    context = {
        'coil_list': material
    }
    return render(request, "production/coil_list.html", context)





# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# python functions
def create_reconsiliation_1(material):

    produced_tonage = 0
    running_meters = 0

    pieces = Piece.objects.filter(coil= material)
    material_list = Cut_Material.objects.filter(coil_number= material.coil_number,
                                                coil_gauge= material.coil_gauge,
                                                coil_width= material.coil_width,
                                                coil_finish= material.coil_finish,
                                                coil_colour= material.coil_colour
                                                )
                   
    final_mass = material_list.aggregate(final_mass = Min('final_mass'))['final_mass']

    initial_mass = 0
    initial_running_meters = 0

    coil = Coil.objects.filter(coil_number=material.coil_number,
                                coil_colour=material.coil_colour,
                                coil_width=material.coil_width,
                                coil_gauge= material.coil_gauge,
                                coil_finish= material.coil_finish
                                )
    if coil:
        initial_mass = coil.initial_mass
        initial_running_meters = coil.initial_running_meters
    else:
        initial_mass = 0
        initial_running_meters = 0

    for material in material_list:
        pieces = Piece.objects.filter(coil=material)
        if pieces:
            produced_tonage +=  pieces.aggregate(total_tonage = Sum('total_tonage'))['total_tonage']
            running_meters += pieces.aggregate(total_running_meters = Sum('total_running_meters'))['total_running_meters']
        else:
            produced_tonage = 0
            running_meters = 0

    mass_gain = produced_tonage *1000 - (initial_mass - final_mass)
    running_meters_gain = running_meters - initial_running_meters
    

    try:
        reconsiliation = Reconsiliation.objects.get(coil_number= material.coil_number,
                                                    coil_gauge= material.coil_gauge,
                                                    coil_width= material.coil_width,
                                                    coil_finish= material.coil_finish,
                                                    coil_colour= material.coil_colour)

        reconsiliation.produced_running_meters = int(running_meters)
        reconsiliation.produced_mass = produced_tonage * 1000
        reconsiliation.mass_gain = mass_gain
        reconsiliation.initial_mass = initial_mass
        reconsiliation.final_mass = final_mass
        reconsiliation.running_meters_gain = running_meters_gain
        reconsiliation.save()

    except Reconsiliation.DoesNotExist:

        Reconsiliation.objects.create(coil_number=material.coil_number,
                                coil_colour=material.coil_colour,
                                coil_width=material.coil_width,
                                coil_gauge= material.coil_gauge,
                                coil_finish= material.coil_finish,
                                initial_mass= initial_mass,
                                final_mass= final_mass,
                                initial_running_meters = initial_running_meters,
                                produced_running_meters= running_meters,
                                produced_mass= produced_tonage,
                                mass_gain= mass_gain,
                                running_meters_gain=running_meters_gain)
    return None





# CLASS BASED VIEWS

class CreateOrderView(CreateView):
    template_name = "production/order_form copy.html"


def create_order_tonage(order):
    pieces = Piece.objects.filter(order=order)
    total_tonage = pieces.values().aggregate(total_tonage=Sum('total_tonage'))['total_tonage']
    if total_tonage is not None:
        total_tonage = total_tonage
    else:
        total_tonage =0
    order.order_tonage = total_tonage
    order.save()
    return None


def update_coil_mass(coil):
    ## this can run after deletion

    supply_chain_coil = Coil.objects.get(coil_number=coil.coil_number,
                                        coil_gauge=coil.coil_gauge,
                                        coil_width=coil.coil_width,
                                        coil_colour=coil.coil_colour,
                                        coil_finish= coil.coil_finish)

    previous_coil_usage = Cut_Material.objects.filter(coil_number=coil.coil_number,
                                                        coil_gauge=coil.coil_gauge,
                                                        coil_width=coil.coil_width,
                                                        coil_colour=coil.coil_colour,
                                                        coil_finish= coil.coil_finish)
    least_mass = 0

    if previous_coil_usage:
        least_mass = previous_coil_usage.aggregate(final_mass=Min('final_mass'))['final_mass']
    else:
        least_mass = supply_chain_coil.initial_mass

    supply_chain_coil.final_mass = least_mass
    supply_chain_coil.save()
    return None

        
def create_reconsiliation(material_number, material_gauge, material_width,
                            material_colour, material_finish):
    # create reconsiliation if new and save it in an instance:
    # 1. get all the coil details from supply chain "Coil" models
    supply_chain_coil = Coil.objects.get(coil_number = material_number,
                                        coil_gauge = material_gauge,
                                        coil_width = material_width,
                                        coil_colour= material_colour,
                                        coil_finish= material_finish)
    
    try:
        coil_reconsiliation = Reconsiliation.objects.get(coil_number = material_number,
                                                        coil_gauge = material_gauge,
                                                        coil_width = material_width,
                                                        coil_colour= material_colour,
                                                        coil_finish= material_finish
                                                        )
        #initial_mass will be got from the cupply chain coil along with the initial_running meters
        # and the final mass
        initial_mass = supply_chain_coil.initial_mass
        final_mass = supply_chain_coil.final_mass
        initial_running_meters = supply_chain_coil.initial_running_meters
        # Next, we start the calculations
        # a. List all the cut material that used the coil
        material_list = Cut_Material.objects.filter(coil_number = material_number,
                                                    coil_gauge = material_gauge,
                                                    coil_width = material_width,
                                                    coil_colour= material_colour,
                                                    coil_finish= material_finish)
        # b. If material was used, we can get pieces
        produced_mass=0
        produced_running_meters=0
        mass_gain=0
        running_meters_gain=0

        if material_list:
            pieces = Piece.objects.filter(coil__in = material_list)
            if pieces:
                produced_mass = pieces.aggregate(total_tonage = Sum('total_tonage'))['total_tonage']*1000
                produced_running_meters = pieces.aggregate(total_running_meters = Sum('total_running_meters'))['total_running_meters']              
                mass_gain = int(produced_mass) - initial_mass
                running_meters_gain = produced_running_meters - initial_running_meters
            else:
                produced_mass=0
                produced_running_meters=0
                mass_gain=0
                running_meters_gain=0
        else:
            produced_mass=0
            produced_running_meters=0
            mass_gain=0
            running_meters_gain=0

        # coil_reconsiliation.initial_running_meters = initial_running_meters
        # coil_reconsiliation.initial_mass = initial_mass
        coil_reconsiliation.produced_mass = produced_mass
        coil_reconsiliation.produced_running_meters = produced_running_meters
        coil_reconsiliation.mass_gain = mass_gain
        coil_reconsiliation.running_meters_gain = running_meters_gain
        coil_reconsiliation.save()
        
    except Reconsiliation.DoesNotExist:
        # produced_mass = supply_chain_coil.initial_mass - supply_chain_coil.final_mass
        coil_reconsiliation = Reconsiliation.objects.create(coil_number = material_number,
            coil_gauge = material_gauge, coil_width = material_width,
            coil_colour= material_colour, coil_finish= material_finish,
            initial_mass = supply_chain_coil.initial_mass, final_mass=supply_chain_coil.final_mass,
            produced_mass=0, initial_running_meters=supply_chain_coil.initial_running_meters,
            produced_running_meters=0, mass_gain=0, running_meters_gain=0)
    ## look for tonages in pieces and if they are not there, return zero
    return None

@login_required
@allowed_users(allowed_roles=['Admin', 'Supervisor'])
def supervisor_dashboard(request):
    # capacity report
    today = datetime.datetime.now()
    capacity_report = Performance.objects.filter(date=shift_func()['shift_date'], shift=shift_func()['shift'])
    ## orders_report
    orders_report = Order.objects.filter(shift_date=shift_func()['shift_date'], production_type="Work Order")
    ##
    standard_report = list_standard_func(shift_func()['shift_date'])
    
    context = {
                'inventory_report': material_report,
                'capacity_report': capacity_report,
                'orders_report': orders_report,
                'standard_report': standard_report,
    }

    return render(request, 'production/supervisor/dashboard.html', context)

def list_standard_func(date):
    standard_list = Order.objects.filter(production_type__in=["Standard"], 
                                                shift_date=date)

    pieces =Piece.objects.filter(order__in=standard_list)
    report = pieces.values('order__profile','order__order_number','order__order_colour','order__order_finish',
                            'order__order_gauge','order__order_finish').order_by().annotate(pieces=
                                Sum('prime_pieces'), 
                                transferred_pieces_sum=Sum('transferred_pieces'),
                                not_transferred=ExpressionWrapper(
                                                Sum('prime_pieces')-
                                                Sum('transferred_pieces'),
                                                output_field=IntegerField()
                                                )
                                            ).values('order__profile','order__order_number',
                                        'order__order_colour', 'order__order_finish', 
                                        'order__order_gauge', 'order__order_finish',
                                        'pieces','transferred_pieces_sum','not_transferred')
    return report

def material_report_planer():
    date_today = datetime.datetime.now().date()
    bond = Coil.objects.filter(location="Bond")
    production = Coil.objects.filter(location="Production")
    report = bond|production

    inventory_report = report.values('coil_gauge','coil_width', 'coil_colour', 
        'coil_finish').order_by().annotate(
        production =Coalesce(Sum('final_mass', filter=Q(location="Production")),0),
        bond =Coalesce( Sum('final_mass', filter=Q(location="Bond")),0),
        total =Coalesce( Sum('final_mass'),0),
        transferred =Coalesce(Sum('final_mass', filter=Q(location="Production",
            production_transfer_date__date=datetime.datetime.now().date())),0),
        planned = ExpressionWrapper(Sum('final_mass')-Sum('final_mass'), output_field=IntegerField()),
        requested = ExpressionWrapper(Sum('final_mass')-Sum('final_mass'), output_field=IntegerField()),
        gauge = F('coil_gauge'),
        width = F('coil_width'),
        colour = F('coil_colour'),
        finish = F('coil_finish')
        ).values('gauge', 'width', 'colour', 'finish','total', 'bond','requested',
                'transferred', 'production', 'planned').order_by()
    
    plan = ProductionPlan.objects.filter(date = date_today)
    plan_report = plan.values('gauge', 'width', 'colour', 'finish').order_by().annotate(
        total = ExpressionWrapper(Sum('tonage')-Sum('tonage'), output_field=IntegerField()),
        bond = ExpressionWrapper(Sum('tonage')-Sum('tonage'), output_field=IntegerField()),
        requested = ExpressionWrapper(Sum('tonage')-Sum('tonage'), output_field=IntegerField()),
        transferred = ExpressionWrapper(Sum('tonage')-Sum('tonage'), output_field=IntegerField()),
        production = ExpressionWrapper(Sum('tonage')-Sum('tonage'), output_field=IntegerField()),
        planned = ExpressionWrapper(Sum('tonage') * 1000, output_field=IntegerField()),
        ).values('gauge', 'width', 'colour', 'finish','total', 'bond','requested',
                        'transferred', 'production', 'planned').order_by()

    request = MaterialRequest.objects.filter(date = date_today)
    request_report = request.values('gauge', 'width', 'colour', 'finish').order_by().annotate(
        total =  ExpressionWrapper(Sum('tonage')-Sum('tonage'), output_field=IntegerField()),
        bond =  ExpressionWrapper(Sum('tonage')-Sum('tonage'), output_field=IntegerField()),
        requested =  ExpressionWrapper(Sum('tonage') * 1000, output_field=IntegerField()),
        transferred = ExpressionWrapper(Sum('tonage')-Sum('tonage'), output_field=IntegerField()),
        production =  ExpressionWrapper(Sum('tonage')-Sum('tonage'), output_field=IntegerField()),
        planned =   ExpressionWrapper(Sum('tonage')-Sum('tonage'), output_field=IntegerField()),
        ).values('gauge', 'width', 'colour', 'finish','total', 'bond','requested',
                        'transferred', 'production', 'planned').order_by()
    # merge the reports
    report = chain(plan_report, request_report)
    report = list(chain(inventory_report, report))
    
    final_report = chain(inventory_report, request_report)
    final_report = chain(final_report, plan_report)
    final_report = pd.DataFrame(final_report)
    final_report = final_report.groupby(
                        ['gauge', 'width', 'colour', 'finish']
                    ).sum().reset_index()
    final_report['after_plan'] = final_report['total'] - final_report['planned']
    final_report = final_report.to_dict('r')
            
    reports = {'request':request_report,
                'plan': plan_report,
                'inventory': inventory_report,
                'report': final_report}

    return reports
    
