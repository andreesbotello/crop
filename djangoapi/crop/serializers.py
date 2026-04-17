from rest_framework import serializers
from .models import Parcelas, LineasRiego, Plantas


class ParcelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelas
        fields = ['id', 'dueno', 'area', 'perimetro', 'cultivo', 'fecha_siembra', 'fecha_creacion']


class LineasRiegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineasRiego
        fields = ['id', 'material', 'estado', 'diametro_pulg', 'longitud_m', 'fecha_creacion']


class PlantasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantas
        fields = ['id', 'variedad', 'estado_salud', 'fecha_cosecha_est', 'fecha_creacion']
