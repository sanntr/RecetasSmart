from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecetaForm, RecetaProductoFormSet
from .models import Receta
from django.http import HttpResponse
from django.template import loader
# Create your views here.
@login_required(login_url='/usuarios/iniciar_sesion/')
def crear_receta(request):
    if request.method == 'POST':
        receta_form = RecetaForm(request.POST)
        formset = RecetaProductoFormSet(request.POST, prefix="productos")

        if receta_form.is_valid() and formset.is_valid():
            receta = receta_form.save(commit=False)
            receta.familia = request.user.familia
            receta.save()

            # Guardar productos asociados
            productos = formset.save(commit=False)
            for producto in productos:
                producto.receta = receta
                producto.save()

            return redirect('listar_recetas')  # Redirige al listado de recetas
    else:
        receta_form = RecetaForm()
        formset = RecetaProductoFormSet(prefix="productos")

    # Cargar el template con loader
    template = loader.get_template('crear_receta.html')
    context = {
        'receta_form': receta_form,
        'formset': formset
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/usuarios/iniciar_sesion/')
def listar_recetas(request):
    recetas = Receta.objects.filter(familia=request.user.familia)

    template = loader.get_template('listar_recetas.html')
    context = {
        'recetas': recetas
    }
    return HttpResponse(template.render(context, request))