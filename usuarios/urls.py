from django.urls import path
from . import views

urlpatterns = [
   path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
   path('iniciar_sesion/', views.iniciar, name='iniciar_sesion'),
   path('salir/', views.salir, name='salir'),
   path('crear_familia/', views.crear_familia, name='crear_familia'),
]