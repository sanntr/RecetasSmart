from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Familia(models.Model):
    nombre = models.CharField(max_length=100)

class Usuario(AbstractUser):
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, null=True, blank=True)
    es_admin_familia = models.BooleanField(default=False)

