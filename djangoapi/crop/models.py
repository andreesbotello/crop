from django.db import models
from django.contrib.gis.db import models as gis_models

#in windows. You don have GEOS
# Create your models here.
class Parcelas(models.Model):
    dueno = models.CharField(max_length=100, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    perimetro = models.FloatField(blank=True, null=True)
    cultivo = models.CharField(max_length=30, blank=True, null=True)
    fecha_siembra = models.DateTimeField(blank=True, null=True)
    geom = gis_models.PolygonField(srid=25830, blank=True, null=True)
