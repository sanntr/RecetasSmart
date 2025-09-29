from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecetaForm, RecetaProductoFormSet
from .models import Receta, RecetaProducto, HistoricoReceta
from django.http import HttpResponse
from django.template import loader
# Create your views here.

@login_required(login_url='/usuarios/iniciar_sesion/')
def crear_receta(request):
    if request.method == 'POST':
        receta_form = RecetaForm(request.POST)
        if receta_form.is_valid():
            receta = receta_form.save(commit=False)
            receta.familia = request.user.familia
            receta.save()

            formset = RecetaProductoFormSet(request.POST, instance=receta)

            if formset.is_valid():
                formset.save()
                return HttpResponse(status=201, content="Receta creada exitosamente.")
        else:
            formset = RecetaProductoFormSet(request.POST) 

    else:
        receta_form = RecetaForm()
        formset = RecetaProductoFormSet()

    template = loader.get_template('crear_receta.html')
    context = {
        'receta_form': receta_form,
        'formset': formset
    }
    return HttpResponse(template.render(context, request))
@login_required(login_url='/usuarios/iniciar_sesion/')
def listar_recetas(request):
    if request.method == "POST":
        receta_id = request.POST.get("receta_id")
        receta = get_object_or_404(Receta, id=receta_id, familia=request.user.familia)
        receta.delete()

    recetas = Receta.objects.filter(familia=request.user.familia)

    template = loader.get_template('listar_recetas.html')
    context = {
        'recetas': recetas
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/usuarios/iniciar_sesion/')
def mostrar_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id, familia=request.user.familia)
    productos = receta.recetaproducto_set.all()
    mensaje = None  

    if request.method == "POST":
        for rp in productos:
            if rp.producto and rp.producto.cantidad_disponible < rp.cantidad_uso:
                mensaje = f"❌ No se pudo ejecutar la receta. Stock insuficiente para {rp.producto.nombre_producto}."
                break

        if not mensaje:  
            for rp in productos:
                if rp.producto:
                    rp.producto.cantidad_disponible -= rp.cantidad_uso
                    rp.producto.save()

            HistoricoReceta.objects.create(receta=receta, cantidad_receta=1)
            mensaje = "✅ Receta ejecutada con éxito."

    template = loader.get_template("mostrar_receta.html")
    context = {
        "receta": receta,
        "productos": productos,
        "message": mensaje
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/usuarios/iniciar_sesion/')
def historico_recetas(request):
    historicos = HistoricoReceta.objects.filter(
        receta__familia=request.user.familia  
    ).select_related("receta").order_by("-fecha")

    template = loader.get_template("historico_recetas.html")
    context = {
        "historicos": historicos
    }
    return HttpResponse(template.render(context, request))