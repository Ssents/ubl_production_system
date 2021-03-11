from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    # path('<int:machine_id>/production-form', views.index, name="production-form"),
    path('search/', views.dashboard_search, name='dashboard_search'),

    # order CRUD
    path('<int:machine_id>/order-form', views.create_order_page, name="create-order-page"),
    path('<int:machine_id>/create-order/', views.create_order, name='create-order'),
    path('edit-order-page/<int:order_id>/', views.edit_order_page, name="edit-order-page"),
    path('edit-order', views.edit_order, name="edit-order"),
    path('delete-order/<int:order_id>/', views.delete_order, name="delete-order"),


    # pieces CRUD
    path('<int:machine_id>/order/<int:order_id>/coil/<int:coil_id>/pieces/', 
        views.pieces_template, name="pieces-template"),
    path('<int:machine_id>/order/<int:order_id>/coil/<int:coil_id>/create-pieces', 
        views.create_pieces, name='create-pieces'),
    path('<int:machine_id>/order/<int:order_id>/coil/list-pieces', 
        views.list_pieces, name='list-pieces'),
    path('piece/update/',  views.update_piece, name='piece_update'),
    path('piece/delete/',  views.delete_piece, name='piece_delete'),

    # coil CRUD
    path('<int:machine_id>/create-order/<int:order_id>/create-coil/', 
        views.create_coil, name='create-coil'),
    path('edit-material-page/<int:order_id>/', views.edit_material_page, 
            name="edit-material-page"),
    # path('edit-material', views.edit_material, name='edit-material'),

    path('material/', views.material_page, name='view-material'),
    path('create-material/', views.create_material_ajax, name='create-material-ajax'),
    path('delete-material/', views.delete_material_ajax, name='delete-material-ajax'),
    path('edit-material/', views.edit_material_ajax, name='edit-material-ajax'),

    # supervisor
    path('standard-list', views.list_products, name="list_products"),
    path('order-list/<str:profile>/<str:order_number>/<str:order_gauge>/<str:order_colour>/<str:order_finish>/', views.list_production_details, name="list-orders"),
    path('transfer-material/<int:piece_id>', views.transfer_material, name="transfer_material"),
    path('transfer-order/<int:order_id>', views.transfer_order, name="transfer_order"),
    path('reverse-material/<int:piece_id>', views.reverse_transfer, name="reverse_transfer"),
    path('supervisor-dashboard/', views.supervisor_dashboard, name="supervisor_board"),

    # plan
    path('planer/', views.planer, name="planer"),
    path('create-plan/', views.create_plan, name="create_plan"),
    path('edit-plan/', views.edit_plan, name="edit_plan"),
    path('delete-plan/', views.delete_plan, name="delete_plan"),
    path('search-production-plan', views.search_production_plan, name='search_production_plan'),

    #manpower 
    path('manpower/', views.ManpowerPlanListView.as_view(), name="manpower_list"),
    path('manpower-create/', views.manpower_create, name="manpower_create"),
    path('manpower-edit/', views.manpower_edit, name="manpower_edit"),
    path('manpower-delete/', views.manpower_delete, name="manpower_delete"),

    #request
    path('request_list', views.material_request_list, name="material_request_list"),
    path('request_create', views.material_request_create, name="material_request_create"),

    path('coils-list/', views.material_list, name="coils_list"),

    #search paths
    path('production-search/', views.finished_goods_search, name="finished_goods_search"),
    path('manpower-search/', views.manpower_search_list, name="manpower_search"),

]
