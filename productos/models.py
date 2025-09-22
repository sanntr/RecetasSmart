from django.db import models
from django.utils import timezone
# Create your models here.
class Producto(models.Model):
    class UnidadMedida(models.TextChoices):
        ML="Ml", "Mililitos"
        KG="Kg","Kilogramos"
        UNIDAD="U","Unidad"
    nombre_producto=models.CharField(max_length  =   100)
    cantidad_disponible=models.IntegerField(blank   =   False,    default=0)
    unidad_medida=models.CharField(max_length=10, choices=UnidadMedida.choices,default=UnidadMedida.UNIDAD)

class CompraProducto(models.Model):
    fecha_compra=models.DateField(timezone.now)
    producto=models.ForeignKey(Producto,    on_delete  =   models.CASCADE)
    cantidad_comprada=models.IntegerField(blank =   False)
