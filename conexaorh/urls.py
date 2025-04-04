from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('gestor/', views.gestor_page, name='gestor_page'),
    path('diretor/', views.diretor_page, name='diretor_page'),
    path('presidente/', views.presidente_page, name='presidente_page'),
    path('rh/', views.rh_page, name='rh_page'),
]