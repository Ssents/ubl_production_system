from quality.models import Reconsiliation
from supply_chain.models import Coil
from .models import Cut_Material, Piece
from django.utils import timezone
from django.db.models import (Count, F, Q, Value, Sum, FloatField, Min, Max, 
                                Avg, IntegerField, ExpressionWrapper, DateField)
from django.db.models.functions import Coalesce


def create_reconsiliation_2(material_number, material_gauge, material_width,
                            material_colour, material_finish):
    # get the coil from supply chain
    coil = Coil.objects.get(coil_number=material_number, coil_colour=material_colour,
                            coil_finish=material_finish, coil_gauge=material_gauge,
                            coil_width=material_width)    
    # STEP 1: GET THE VALUES
    # Getting initial values from the cupply chain coil
    initial_mass = coil.initial_mass
    initial_running_meters = coil.initial_running_meters
    final_mass = coil.final_mass
    #initialize the other values
    start_date = timezone.now().date()
    end_date = timezone.now().date()
    
    produced_mass = 0
    produced_running_meters = 0
    mass_gain = 0
    running_meters_gain = 0
    
    # getting tonages from cut material
    material_list = Cut_Material.objects.filter(coil_number=material_number, 
                                                coil_gauge=material_gauge, coil_width=material_width,
                                                coil_colour=material_colour, coil_finish=material_finish)

    # if the coil has been used, 
        # get the material list
    # else
        # initiate all the important values to zero
    if material_list:
        start_date = material_list.order_by('order__shift_date')[0].order.shift_date
        end_date = material_list.order_by('-order__shift_date')[0].order.shift_date
        pieces = Piece.objects.filter(coil__in = material_list)
        if pieces:
            produced_mass = pieces.aggregate(total_tonage = Sum('total_tonage'))['total_tonage']*1000
            produced_running_meters = pieces.aggregate(total_running_meters = Sum('total_running_meters'))['total_running_meters']              
            mass_gain = int(produced_mass) - initial_mass
            running_meters_gain = produced_running_meters - initial_running_meters

    #STEP 2: CREATE OR UPDATE THE RECONSILIATION
    # try:
        # update the values
    # except if it does not exist:
        # create
    try:
        reconsiliation = Reconsiliation.objects.get(coil_number = material_number,
                                                    coil_gauge = material_gauge,
                                                    coil_width = material_width,
                                                    coil_colour= material_colour,
                                                    coil_finish= material_finish)
        reconsiliation.final_mass = final_mass
        reconsiliation.produced_mass = produced_mass
        reconsiliation.produced_running_meters = produced_running_meters
        reconsiliation.mass_gain = mass_gain
        reconsiliation.running_meters_gain = running_meters_gain
        reconsiliation.start_date = start_date
        reconsiliation.finish_date = end_date

    except Reconsiliation.DoesNotExist:
        Reconsiliation.objects.create(
            coil_number = material_number,
            coil_gauge = material_gauge, 
            coil_width = material_width,
            coil_colour = material_colour, 
            coil_finish = material_finish,
            initial_mass = initial_mass, 
            final_mass = final_mass,
            produced_mass = 0, 
            initial_running_meters = initial_running_meters,
            produced_running_meters = 0, 
            mass_gain = 0, 
            running_meters_gain = 0,
            start_date = timezone.now().date(), 
            finish_date = timezone.now().date()
        )
    return "SUCCESS"
