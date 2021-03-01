from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# import frontend_choices
from frontend_choices import (PRODUCTION_BOND_CHOICES, PRODUCTION_TYPE_CHOICES, 
                                PROFILE_CHOICES, ORDER_COLOUR_CHOICES,
                                ORDER_FINISH_CHOICES, ORDER_GAUGE_CHOICES,
                                 ORDER_WIDTH_CHOICES)
from maintenance.models import Machine
from production.models import Order, Cut_Material, Piece, Performance

from django.db.models import Count, F, Value, Sum, FloatField
from production.decorators import allowed_users

import datetime


# Create your views here.
@login_required
@allowed_users(allowed_roles=['Admin', 'Operator', 'Production Supervisor'])
def machines(request):
    machines_list = Machine.objects.all()

    paginator = Paginator(machines_list, 8)
    page = request.GET.get('page')
    paged_machines_list = paginator.get_page(page)


    context = {
        'machines': paged_machines_list
    }
    return render(request, "maintenance/machines.html", context)

@login_required
@allowed_users(allowed_roles=['Admin', 'Operator', 'Production Supervisor'])
def machine(request, machine_id):

    date_today = datetime.datetime.now()
    today_day = date_today.day
    today_month = date_today.month
    today_year = date_today.year

    machinery = get_object_or_404(Machine, pk=machine_id)

    time_now = datetime.datetime.now().time()
    today=datetime.datetime.now()
    shift=""
    machine_target = 0

    shift_dict = shift_func()
    shift = shift_dict["shift"]
    shift_date = shift_dict['shift_date']
    machine_target = shift_dict['hours'] * machinery.machine_hourly_capacity



    order_list = Order.objects.filter(shift_date = shift_date,
                                    shift=shift, machine=machinery).values()
    ##query for tonage today
    piece = Piece.objects.all()
    total_tonage = order_list.values().order_by().aggregate(
                                tonage=Sum('piece__total_tonage'))['tonage']

    if total_tonage is not None:
        total_tonage = total_tonage
    else:
        total_tonage = 0

    machine_capacity(machinery, date_today.date() , shift, total_tonage)


    context = {
        'machinery':machinery,
        'bond': PRODUCTION_BOND_CHOICES,
        'colour': ORDER_COLOUR_CHOICES,
        'finish': ORDER_FINISH_CHOICES,
        'gauge': ORDER_GAUGE_CHOICES,
        'width': ORDER_WIDTH_CHOICES,
        'order_list': order_list,
        'day':  today_day,
        'month': today_month,
        'year': today_year,
        'date': date_today.date(),
        'total_tonage': total_tonage,
        'machine_target': machine_target,
    }

    return render(request, 'production/dashboard.html', context)

def machine_capacity(machine, date, shift, total_tonage):
    try:
        # performance = get_object_or_404(Performance, machine=machine, date=date, shift=shift)
        performance = Performance.objects.get(machine=machine, date=date, shift=shift)
        performance.machine = machine
        performance.date = date
        performance.shift = shift
        performance.machine_hourly_capacity = machine.machine_hourly_capacity
        if shift=="Day":
            performance.shift_hours = 8
        else:
            performance.shift_hours = 11
        performance.total_capacity = performance.shift_hours * performance.machine_hourly_capacity
        performance.total_production = total_tonage
        performance.percentage = total_tonage/ performance.total_capacity
        performance.save()

    except Performance.DoesNotExist:

        if shift=="Day":
            shift_hours = 8
        else:
            shift_hours = 11

        machine_hourly_capacity = machine.machine_hourly_capacity
        total_capacity = machine_hourly_capacity * shift_hours
        percentage = total_tonage / total_capacity


        Performance.objects.create( machine = machine,
                                    date = date, shift = shift,
                                    machine_hourly_capacity = machine_hourly_capacity,
                                    shift_hours = shift_hours, 
                                    total_capacity = total_capacity,
                                    total_production= total_tonage,
                                    percentage = percentage)

    return None

def shift_func():
    today = datetime.datetime.now()
    time_now = datetime.datetime.now().time()

    if time_now > datetime.time(8,0,0,0) and time_now < datetime.time(17, 30, 0, 0):
        shift = "Day"
        shift_date = datetime.datetime(today.year, today.month, today.day).date()
        hours = 8
    elif time_now > datetime.time(0,0,0,0) and time_now < datetime.time(8, 0, 0, 0):
        shift = "Night"
        shift_date = datetime.datetime(today.year, today.month, today.day-1).date()
        hours = 11
    else:
        shift = "Night"
        shift_date = datetime.datetime(today.year, today.month, today.day).date()
        hours =11
    return {"shift":shift, "shift_date":shift_date, "hours":hours}