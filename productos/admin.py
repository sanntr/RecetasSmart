from django.contrib import admin
from . import models

#lista de modelos
modelos= [models.Producto, models.CompraProducto]

# Register your models here.
admin.site.register(modelos)