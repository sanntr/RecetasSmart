from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .forms import crear_usuarios, iniciar_sesion, crear_familia as form_familia
from .models import Familia, Usuario 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

# Vista para crear un nuevo usuario
@login_required(login_url='/usuarios/iniciar_sesion/')
def crear_usuario(request):
    verificacion =verificar_admin(request)
    if verificacion:
        return verificacion
    form = crear_usuarios.UsuarioForm()

    if request.method == 'POST':
        form = crear_usuarios.UsuarioForm(request.POST)
        if form.is_valid():
            usuario = Usuario(
                first_name=form.cleaned_data['nombre'],
                last_name=form.cleaned_data['apellido'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['usuario'],
                family_id=request.user.familia_id
            )
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            #Esto se debe cambiar para que redirecione a la pagina inicial de la familia
            return HttpResponse(status=201, content="Usuario creado exitosamente.")
        
    template = loader.get_template('crear_usuario.html')
    
    return HttpResponse(status=200,content= template.render({'form':form}, request))

# Vista para iniciar sesión
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
                # Se debe cambiar para que redireccione a la pagina inicial de la familia
                return HttpResponse(status=200, content="Inicio de sesión exitoso.")
            else:
                mensaje = "Usuario o contraseña incorrectos."
                form.add_error(None, "Usuario o contraseña incorrectos.")
                return HttpResponse(status=200, content=loader.get_template('inicio_sesion.html').render({'form': iniciar_sesion.IniciarSesionForm(), 'message': mensaje}, request))
    return HttpResponse(status=200, content=loader.get_template('inicio_sesion.html').render({'form': iniciar_sesion.IniciarSesionForm()}, request))


# Vista para cerrar sesión
@login_required(login_url='/usuarios/iniciar_sesion/')
def  salir(request):
    logout(request)
    return redirect('/usuarios/iniciar_sesion/')

# Vista para crear una nueva familia
def crear_familia(request):
    form = form_familia.FamiliaAdminForm()
    if request.method == 'POST':
        form = form_familia.FamiliaAdminForm(request.POST)
        if form.is_valid():
            familia=Familia.objects.create(nombre=form.cleaned_data['nombre_familia'])
            
            usuario = Usuario.objects.create_user(
                username=form.cleaned_data['usuario'],
                first_name=form.cleaned_data['nombre'],
                last_name=form.cleaned_data['apellido'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                familia=familia,
                es_admin_familia=True
            )

            login(request, usuario)

            #Se debe cambiar para que redireccione a la pagina inicial de la familia
            return HttpResponse(status=201, content="Familia creada exitosamente.")
    return HttpResponse(status=200, content=loader.get_template('crear_familia.html').render({'form': form}, request))

# Vista para listar usuarios de la familia al administrador
@login_required(login_url='/usuarios/iniciar_sesion/')
def listar_usuarios(request):
    verificar=verificar_admin(request)
    if verificar:
        return verificar
    usuarios = Usuario.objects.filter(familia=request.user.familia, is_active=True, es_admin_familia=False)
    return HttpResponse(status=200, content=loader.get_template('listar_usuarios.html').render({'usuarios': usuarios}, request))

# Vista para eliminar un usuario (desactivar)
@login_required(login_url='/usuarios/iniciar_sesion/')
def eliminar_usuario(request, usuario_id):
    verificar = verificar_admin(request)
    if verificar:
        return verificar
    try:
        usuario = Usuario.objects.get(id=usuario_id, familia=request.user.familia)
        usuario.is_active = False
        usuario.save()
        return HttpResponse(status=204)
    except Usuario.DoesNotExist:
        return HttpResponse(status=404)

#funciones auxiliares
def verificar_admin(request):
    if not request.user.es_admin_familia:
        return HttpResponse(status=403, content=loader.get_template('acceso_denegado.html').render({}, request))
