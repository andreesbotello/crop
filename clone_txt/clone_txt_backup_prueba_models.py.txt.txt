from django.db import models
from django.contrib.gis.db import models as gis_models

class Buildings(models.Model):
    description = models.TextField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    geom = gis_models.PolygonField(srid=25830, blank=True, null=True)

    class Meta:
        db_table = 'd"."buildings'
        managed = False 