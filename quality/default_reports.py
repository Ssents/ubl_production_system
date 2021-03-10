from django.views import View
from django.db.models.functions import Coalesce
from django.db.models import (Count, F, Q, Value, Sum, FloatField, Min, Max, DecimalField,
                                Avg, IntegerField, ExpressionWrapper, DateField, CharField)

from production.models import Piece
from .models import Coil_description, Reconsiliation

import datetime

class ProductionReports(View):
    ppaz_colours = Coil_description.objects.filter(
                                                        coil_type="PPAZ"
                                                    ).values_list("coil_colour")
    az_colour = Coil_description.objects.filter(
                                                coil_type="AZ"
                                                ).values_list("coil_colour")
    today_month = datetime.datetime.now().month

    def get_monthly_report(self, month=today_month):
        monthly_production_tonage = Piece.objects.filter(order__shift_date__year = datetime.datetime.now().year
            ).values('order__shift_date__month'
            ).order_by('order__shift_date__month').annotate(
            ppaz_prime_tonage = Coalesce(Sum('prime_tonage', 
                                    filter=Q(order__order_colour__in = self.ppaz_colours)),0),
            ppaz_rejects_tonage = Coalesce(Sum('rejects_tonage', 
                                    filter=Q(order__order_colour__in = self.ppaz_colours)),0),
            az_prime_tonage = Coalesce(Sum('prime_tonage', 
                                    filter=Q(order__order_colour__in = self.az_colour)),0),
            az_rejects_tonage = Coalesce(Sum('rejects_tonage', 
                                    filter=Q(order__order_colour__in = self.az_colour)),0),
            total = Coalesce(ExpressionWrapper(
                        Sum('prime_tonage') + Sum('rejects_tonage')
                    , output_field=DecimalField()), 0)
            ).values("order__shift_date__month", "ppaz_prime_tonage", "ppaz_rejects_tonage",
                    "az_prime_tonage", "az_rejects_tonage", "total"
                    )
        return monthly_production_tonage

    def get_daily_report(self):
        month = datetime.datetime.now().month
        daily_tonage_report = Piece.objects.filter(order__shift_date__month= month
            ).values('order__shift_date__month', 'order__shift_date__day'
            ).order_by(
                'order__shift_date__day'
            ).annotate(
            ppaz_prime_tonage = Coalesce(Sum('prime_tonage', 
                filter=Q(order__order_colour__in = self.ppaz_colours)),0),
            ppaz_rejects_tonage = Coalesce(Sum('rejects_tonage', 
                filter=Q(order__order_colour__in = self.ppaz_colours)),0),
            az_prime_tonage = Coalesce(Sum('prime_tonage', 
                filter=Q(order__order_colour__in = self.az_colour)),0),
            az_rejects_tonage = Coalesce(Sum('rejects_tonage', 
                filter=Q(order__order_colour__in = self.az_colour)),0),
            total = Coalesce(ExpressionWrapper(
                        Sum('prime_tonage') + Sum('rejects_tonage')
                    , output_field=DecimalField()), 0)
            ).values("order__shift_date__month","order__shift_date__day", "ppaz_prime_tonage",
                "ppaz_rejects_tonage", "az_prime_tonage", "az_rejects_tonage", "total"
            )
                    
        return daily_tonage_report

    def get(self):
        context = {
            "testing": "yeah",
            "monthly_tonage_report": self.get_monthly_report(),
            "date": datetime.datetime.now().date(),
            "daily_tonage_report": self.get_daily_report(),
            "reconsiliation": self.get_reconsiliation_report(),
        }
        return context
     
    def get_reconsiliation_report(self):
        month = self.today_month
        monthly_reconsiliation = Reconsiliation.objects.filter(start_date__month=month).values()
        return monthly_reconsiliation



