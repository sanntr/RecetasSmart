from django.db import models
from productos.models import Producto
from django.utils import timezone
from usuarios.models import Familia
# Create your models here.

class Receta(models.Model):
    titulo=models.CharField(max_length=120, blank=False)
    pasos_receta=models.TextField(null=True)
    productos=models.ManyToManyField(Producto,through="RecetaProducto")
    familia=models.ForeignKey(Familia, on_delete=models.CASCADE)
    
#tabla intermediaria
class RecetaProducto(models.Model):
    producto=models.ForeignKey(Producto, on_delete=models.SET_NULL,null=True,blank=True)
    receta=models.ForeignKey(Receta,on_delete=models.CASCADE)
    cantidad_uso=models.IntegerField(null=False)

class HistoricoReceta(models.Model):
    fecha=models.DateTimeField(default=timezone.now)
    receta=models.ForeignKey(Receta,blank=False, on_delete=models.CASCADE)
    cantidad_receta=models.IntegerField(default=1)