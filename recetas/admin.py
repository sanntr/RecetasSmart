from django.contrib import admin
from . import models

#lista de modelos
modelos= [models.Receta, models.RecetaProducto, models.HistoricoReceta]

# Register your models here.
admin.site.register(modelos)