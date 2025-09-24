from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import crear_usuarios, iniciar_sesion
from .models import Usuario 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/usuarios/iniciar_sesion/')
def crear_usuario(request):

    form = crear_usuarios.UsuarioForm()

    if request.method == 'POST':
        form = crear_usuarios.UsuarioForm(request.POST)
        if form.is_valid():
            usuario = Usuario(
                first_name=form.cleaned_data['nombre'],
                last_name=form.cleaned_data['apellido'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['usuario']
            )
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            #Esto se debe cambiar para que redirecione a la pagina inicial de la familia
            return HttpResponse(status=201, content="Usuario creado exitosamente.")
        
    template = loader.get_template('crear_usuario.html')
    
    return HttpResponse(status=200,content= template.render({'form':form}, request))


def  iniciar(request):
    form = iniciar_sesion.IniciarSesionForm()
    if request.method == 'POST':
        form = iniciar_sesion.IniciarSesionForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            password = form.cleaned_data['password']
            user = authenticate(request,username=usuario, password=password)
            if user is not None:
                login(request, user)
                # Redirigir a la página de inicio o a la página deseada después del inicio de sesión exitoso
                return HttpResponse(status=200, content="Inicio de sesión exitoso.")
            else:
                form.add_error(None, "Usuario o contraseña incorrectos.")
    return HttpResponse(status=200, content=loader.get_template('inicio_sesion.html').render({'form': iniciar_sesion.IniciarSesionForm()}, request))