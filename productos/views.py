from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm , AumentarStockForm
from django.contrib import messages
from .models import Producto
# Create your views here.
def principal(request):
    template = loader.get_template('search.html')
    return HttpResponse(template.render())

@login_required(login_url='/usuarios/iniciar_sesion/')
def crear_producto(request):
    form = ProductoForm()

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            producto = Producto(
                nombre_producto=cd['nombre_producto'],
                cantidad_disponible=cd['cantidad_disponible'],
                unidad_medida=cd['unidad_medida'],
                familia=request.user.familia 
            )
            producto.save()
            return redirect('home')  # Redirige a la página principal o a donde desees después de crear el producto
    template = loader.get_template('crear_producto.html')
    return HttpResponse(template.render({'form': form}, request))

@login_required(login_url='/usuarios/iniciar_sesion/')
def listar_productos(request):
    productos = Producto.objects.filter(familia=request.user.familia)  # Solo los de la familia del usuario
    return render(request, 'listar_productos.html', {'productos': productos})


@login_required(login_url='/usuarios/iniciar_sesion/')
def aumentar_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, familia=request.user.familia)

    if request.method == "POST":
        form = AumentarStockForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            producto.cantidad_disponible += cantidad
            producto.save()
            messages.success(request, f"✅ Stock de {producto.nombre_producto} aumentado en {cantidad}. Ahora tiene {producto.cantidad_disponible}.")
            return redirect("listar_productos")  # ajusta al nombre de tu vista de productos
    else:
        form = AumentarStockForm()

    return render(request, "aumentar_stock.html", {"form": form, "producto": producto})