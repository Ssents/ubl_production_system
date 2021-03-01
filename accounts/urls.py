from django.urls import path
from accounts import views



urlpatterns = [
    path('login/', views.login, name='login'),
    path('register-page/', views.register_user_page, name='register-page'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]