from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from usuarios.models import Usuario, Familia
from productos.models import Producto
from recetas.models import Receta
from django.contrib.auth.decorators import login_required      
# Create your views here.

@login_required(login_url='/usuarios/iniciar_sesion/')
def home(request):
    template = loader.get_template('inicio.html')
    familia=request.user.familia_id
    productos=Producto.objects.filter(familia_id=familia)
    recetas=Receta.objects.filter(familia_id=familia)
    familia_nombre=Familia.objects.get(id=familia).nombre
    return HttpResponse(template.render({'productos': productos, 'recetas': recetas, 'familia': familia_nombre}, request))
