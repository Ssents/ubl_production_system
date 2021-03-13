from django.shortcuts import render
from django.views import View
from django.views.generic import (TemplateView, ListView, DetailView )

from .default_reports import  ProductionReports

from production.models import Order, Cut_Material, Piece
from .models import Reconsiliation

from frontend_choices import MONTH_LIST_CHOICES, YEAR_LIST_CHOICES

import calendar
import datetime

class DashboardView(ProductionReports):
    template_name = "quality/dashboard.html"

    def get(self,request):
        context = super(DashboardView, self).get()
        context["daily_tonage_report"] = super(DashboardView, self).get_daily_report()
        return render(request, self.template_name, context)

class ReconsiliationListView(ListView):
    template_name = "quality/reconsiliation_list.html"
    model = Reconsiliation
    context_object_name = "monthly_reconsiliation_list"

    def get_context_data(self):
        context = super().get_context_data()
        context["year"] = datetime.datetime.now().year
        context["month"] = calendar.month_abbr[int(datetime.datetime.now().month)]
        context["years_list"] = YEAR_LIST_CHOICES
        context["months_list"] = MONTH_LIST_CHOICES
        return context

    def get_queryset(self, month=datetime.datetime.now().month, 
        year=datetime.datetime.now().year):
        return Reconsiliation.objects.filter(start_date__month= month,
            start_date__year=year).order_by(
            'coil_gauge','coil_colour', 'coil_finish', 'coil_width'
        )

class ReconsiliationDetaillView(DetailView):
    model = Reconsiliation
    template_name = "quality/reconsiliation_detail.html"
    context_object_name = "reconsiliation_detail"

    def get_context_data(self, **kwargs):
        context = super(ReconsiliationDetaillView, self).get_context_data(**kwargs)
        reconsiliation = Reconsiliation.objects.get(pk=self.kwargs.get('pk'))
        cut_material = Cut_Material.objects.filter(coil_number=reconsiliation.coil_number)
        context['pieces'] = Piece.objects.filter(coil__in = cut_material)
        return context

class SearchDailyTonageView(ProductionReports):
    template_name = "quality/dashboard.html"
    model = Reconsiliation
    context_object_name = "monthly_reconsiliation_list"

    def post(self, request):
        if request.method=="POST":
            month = request.POST['search_month']
            year = request.POST['search_year']
            reconsiliation_list = Reconsiliation.objects.filter(start_date__month = int(month),
                start_date__year = int(year))
            context = super(SearchDailyTonageView, self).get()
            context["daily_tonage_report"] = super().get_daily_report(month=int(month), 
                year=int(year))
            context["month"] = calendar.month_abbr[int(month)]
            context["year"] = int(year)
            return render (request, self.template_name, context)

class SearchMonthlyReconsiliationView(ProductionReports):
    template_name = "quality/reconsiliation_list.html"
    model = Reconsiliation
    
    def post(self, request):
        if request.method=="POST":
            search_month = request.POST['search_month']
            search_year = request.POST['search_year']
            context = super().get()
            context["year"] = int(search_year)
            context["month"] = calendar.month_abbr[int(search_month)]
            context["monthly_reconsiliation_list"] = super().get_reconsiliation_report(
                month = search_month, year=search_year
            )
            return render(request, self.template_name, context)        

    
