from django.urls import path
from quality import views
urlpatterns = [
    # path('coil-form/', views.coil_form, name="coil-form"),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('reconsiliation/', views.ReconsiliationListView.as_view(), 
                                                name='reconsiliation'),
    path('reconsiliation/<int:pk>', views.ReconsiliationDetaillView.as_view(), 
                                                name="reconsiliation_detail"),
]