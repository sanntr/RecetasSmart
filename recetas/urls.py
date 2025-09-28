from django.urls import path
from . import views

urlpatterns = [
   path('crear_receta/', views.crear_receta, name='crear_receta'),
    path('listar_recetas/', views.listar_recetas, name='listar_recetas'),
]