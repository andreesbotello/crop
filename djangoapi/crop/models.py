from django.db import models
from django.contrib.gis.db import models as gis_models
import django.utils.timezone as djangoTimezone

#in windows. You don have GEOS
# Create your models here.
class Parcelas(models.Model):
    dueno = models.CharField(max_length=100, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    perimetro = models.FloatField(blank=True, null=True)
    cultivo = models.CharField(max_length=30, blank=True, null=True)
    fecha_siembra = models.DateTimeField(blank=True, null=True)
    geom = gis_models.PolygonField(srid=25830, blank=True, null=True)
    fecha_creacion = models.DateTimeField(db_default=djangoTimezone.now())

class LineasRiego(models.Model):
    material = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    diametro_pulg = models.FloatField(blank=True, null=True)
    longitud_m = models.FloatField(blank=True, null=True)
    geom = gis_models.LineStringField(srid=25830, blank=True, null=True)
    fecha_creacion = models.DateTimeField(db_default=djangoTimezone.now())

class Plantas(models.Model):
    variedad = models.CharField(max_length=50, blank=True, null=True)
    estado_salud = models.CharField(max_length=50, blank=True, null=True)
    fecha_cosecha_est = models.DateTimeField(blank=True, null=True)
    geom = gis_models.PointField(srid=25830, blank=True, null=True)
    fecha_creacion = models.DateTimeField(db_default=djangoTimezone.now())