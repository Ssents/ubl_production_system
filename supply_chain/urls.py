from django.urls import path
from . import views

urlpatterns = [
    path('material-list/', views.material_list_view, name='dashboard'),

    # CRUD
    path('create-coil/', views.create_coil, name='create_coil'),
    path('edit-coil/', views.edit_coil, name='edit_coil'),
    path('delete-coil/', views.delete_coil, name='delete_coil'),
    path('transfer-coil/', views.transfer_coil, name='transfer_coil'),

    #
    path('', views.main_dashboard, name='main_dashboard'),

    # search details
    path('retrieve-coil-details/<str:date>/<str:colour>/<str:finish>/<int:gauge>/<int:width>',
        views.get_coil_details, name='get_coil_details'),
]