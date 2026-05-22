from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
from djangoapi.settings import EPSG_FOR_GEOMETRIES

from .models import Parcelas, LineasRiego, Plantas


class WKTGeometryField(serializers.Field):
    def to_representation(self, value):
        return value.wkt if value else None

    def to_internal_value(self, data):
        if not isinstance(data, str) or not data.strip():
            raise serializers.ValidationError('La geometria debe enviarse como texto WKT.')
        try:
            return GEOSGeometry(data, srid=EPSG_FOR_GEOMETRIES)
        except Exception as exc:
            raise serializers.ValidationError(f'WKT invalido: {exc}')


class ParcelasSerializer(serializers.ModelSerializer):
    geom = WKTGeometryField()

    class Meta:
        model = Parcelas
        fields = ['id', 'dueno', 'area', 'perimetro', 'cultivo', 'fecha_siembra', 'geom', 'fecha_creacion']
        read_only_fields = ['area', 'perimetro', 'fecha_creacion']

    def create(self, validated_data):
        geom = validated_data.get('geom')
        validated_data['area'] = geom.area
        validated_data['perimetro'] = geom.length
        return super().create(validated_data)

    def update(self, instance, validated_data):
        geom = validated_data.get('geom')
        if geom:
            validated_data['area'] = geom.area
            validated_data['perimetro'] = geom.length
        return super().update(instance, validated_data)


class LineasRiegoSerializer(serializers.ModelSerializer):
    geom = WKTGeometryField()

    class Meta:
        model = LineasRiego
        fields = ['id', 'material', 'estado', 'diametro_pulg', 'longitud_m', 'geom', 'fecha_creacion']
        read_only_fields = ['longitud_m', 'fecha_creacion']

    def create(self, validated_data):
        geom = validated_data.get('geom')
        validated_data['longitud_m'] = geom.length
        return super().create(validated_data)

    def update(self, instance, validated_data):
        geom = validated_data.get('geom')
        if geom:
            validated_data['longitud_m'] = geom.length
        return super().update(instance, validated_data)


class PlantasSerializer(serializers.ModelSerializer):
    geom = WKTGeometryField()

    class Meta:
        model = Plantas
        fields = ['id', 'variedad', 'estado_salud', 'fecha_cosecha_est', 'geom', 'fecha_creacion']
