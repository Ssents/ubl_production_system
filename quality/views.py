from django.shortcuts import render
from django.views import View
from django.views.generic import (TemplateView, ListView, DetailView )

from .default_reports import  ProductionReports

from production.models import Order, Cut_Material
from .models import Reconsiliation

import datetime

class DashboardView(ProductionReports):
    template_name = "quality/dashboard.html"

    def get(self,request):
        context = super().get()
        return render(request, self.template_name, context)

class ReconsiliationListView(ListView):
    template_name = "quality/reconsiliation_list.html"
    model = Reconsiliation
    context_object_name = "monthly_reconsiliation_list"

    def get_queryset(self, month=datetime.datetime.now().month):
        return Reconsiliation.objects.filter(start_date__month= month).order_by(
            'coil_gauge','coil_colour', 'coil_finish', 'coil_width'
        )

class ReconsiliationDetaillView(DetailView):
    model = Reconsiliation
    template_name = "quality/reconsiliation_detail.html"
    context_object_name = "reconsiliation_detail"

    def get_context_data(self, **kwargs):
        context = super(ReconsiliationDetaillView, self).get_context_data(**kwargs)
        reconsiliation = Reconsiliation.objects.get(pk=self.kwargs.get('pk'))
        context["orders"] = Cut_Material.objects.filter(coil_number=reconsiliation.coil_number)
        return context

class SearchMonthlyReconsiliationView(ProductionReports, ListView):
    template_name = "quality/reconsiliation_list.html"
    model = Reconsiliation
    context_object_name = "monthly_reconsiliation_list"
