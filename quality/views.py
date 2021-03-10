from django.shortcuts import render
from django.views import View
from django.views.generic import (TemplateView, ListView, DetailView )

from .default_reports import  ProductionReports

import datetime

class DashboardView(ProductionReports):
    template_name = "quality/dashboard.html"

    def get(self,request):
        context = super().get()
        return render(request, self.template_name, context)

