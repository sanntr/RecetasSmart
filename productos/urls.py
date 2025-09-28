from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('listar/', views.listar_productos, name='listar_productos'),
]