from django.urls import path
from . import views

urlpatterns = [
   path('crear_receta/', views.crear_receta, name='crear_receta'),
    path('listar_recetas/', views.listar_recetas, name='listar_recetas'),
    path('mostrar_receta/<int:receta_id>/', views.mostrar_receta, name='mostrar_receta'),
    path('historico_recetas/', views.historico_recetas, name='historico_recetas'),
]