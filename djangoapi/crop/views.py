# Django imports
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict

from rest_framework import viewsets, permissions

from crop.models import Parcelas, LineasRiego, Plantas
from crop.serializers import ParcelasSerializer, LineasRiegoSerializer, PlantasSerializer
from core.myLib.baseDjangoView import BaseDjangoView
from scripts.crop.DjangoModels.parcelas.parcelasDJ import ParcelasDJ
from scripts.crop.DjangoModels.lineas_riego.lineas_riegoDJ import LineasRiegoDJ
from scripts.crop.DjangoModels.plantas.plantasDJ import PlantasDJ

class HelloWorld(View):
    def get(self, request):
        return JsonResponse({"ok": True, "message": "Crop. Hello world", "data": []})


def model_to_wkt_dict(obj):
    data = model_to_dict(obj)
    data['geom'] = obj.geom.wkt if obj.geom else None
    return data


def get_required_wkt(request):
    wkt = request.POST.get('geom', None)
    if not wkt:
        return None, JsonResponse({'ok': False, 'message': 'La geometria WKT en el campo geom es obligatoria', 'data': []}, status=400)
    return wkt, None

#  Parcelas

class ParcelasView(BaseDjangoView):
    """
    View for Parcelas model.

    URLs:
        GET  /crop/parcelas/<action>/           → selectall
        GET  /crop/parcelas/<action>/<id>/      → selectone
        POST /crop/parcelas/insert/             → insert
        POST /crop/parcelas/update/<id>/        → update
        POST /crop/parcelas/delete/<id>/        → delete
    """

    def selectone(self, id):
        l = list(Parcelas.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La parcela {id} no existe', 'data': []}, status=404)
        data = model_to_wkt_dict(l[0])
        return JsonResponse({'ok': True, 'message': 'Parcela recuperada', 'data': [data]}, status=200)

    def selectall(self):
        data = []
        for p in Parcelas.objects.all():
            data.append(model_to_wkt_dict(p))
        return JsonResponse({'ok': True, 'message': 'Datos recuperados', 'data': data}, status=200)

    def insert(self, request):
        geom, error = get_required_wkt(request)
        if error:
            return error

        data = {
            'dueno': request.POST.get('dueno', ''),
            'cultivo': request.POST.get('cultivo', ''),
            'fecha_siembra': request.POST.get('fecha_siembra') or None,
            'geom': geom,
        }
        result = ParcelasDJ().insert(data)
        if not result.get('ok'):
            return JsonResponse({'ok': False, 'message': result.get('message'), 'data': []}, status=400)
        p = Parcelas.objects.get(id=result['id'])
        return JsonResponse({'ok': True, 'message': 'Parcela insertada', 'data': [model_to_wkt_dict(p)]}, status=201)

    def update(self, request, id):
        l = list(Parcelas.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La parcela {id} no existe', 'data': []}, status=404)
        geom, error = get_required_wkt(request)
        if error:
            return error

        data = {
            'id': id,
            'dueno': request.POST.get('dueno', l[0].dueno),
            'cultivo': request.POST.get('cultivo', l[0].cultivo),
            'geom': geom,
        }
        result = ParcelasDJ().update(data)
        if not result.get('ok'):
            return JsonResponse({'ok': False, 'message': result.get('message'), 'data': []}, status=400)
        p = Parcelas.objects.get(id=id)
        return JsonResponse({'ok': True, 'message': 'Parcela actualizada', 'data': [model_to_wkt_dict(p)]}, status=200)

    def delete(self, id):
        l = list(Parcelas.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La parcela {id} no existe', 'data': []}, status=404)
        l[0].delete()
        return JsonResponse({'ok': True, 'message': f'Parcela {id} eliminada', 'data': []}, status=200)


class ParcelasModelViewSet(viewsets.ModelViewSet):
    """
    DRF ModelViewSet for Parcelas.
    Provides list, retrieve, create, update, partial_update and destroy.
    """
    queryset = Parcelas.objects.all()
    serializer_class = ParcelasSerializer
    permission_classes = [permissions.AllowAny]

#  Líneas de riego
class LineasRiegoView(BaseDjangoView):
    def selectone(self, id):
        l = list(LineasRiego.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La linea de riego {id} no existe', 'data': []}, status=404)
        linea = l[0]
        data = model_to_wkt_dict(linea)
        return JsonResponse({'ok': True, 'message': 'Linea de riego recuperada', 'data': [data]}, status=200)

    def selectall(self):
        data = []
        for linea in LineasRiego.objects.all():
            data.append(model_to_wkt_dict(linea))
        return JsonResponse({'ok': True, 'message': 'Datos recuperados', 'data': data}, status=200)

    def insert(self, request):
        geom, error = get_required_wkt(request)
        if error:
            return error

        data = {
            'material': request.POST.get('material', ''),
            'estado': request.POST.get('estado', ''),
            'diametro_pulg': request.POST.get('diametro_pulg') or None,
            'geom': geom,
        }
        result = LineasRiegoDJ().insert(data)
        if not result.get('ok'):
            return JsonResponse({'ok': False, 'message': result.get('message'), 'data': []}, status=400)
        linea = LineasRiego.objects.get(id=result['id'])
        return JsonResponse({'ok': True, 'message': 'Linea de riego insertada', 'data': [model_to_wkt_dict(linea)]}, status=201)

    def update(self, request, id):
        l = list(LineasRiego.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La linea de riego {id} no existe', 'data': []}, status=404)
        geom, error = get_required_wkt(request)
        if error:
            return error

        linea = l[0]
        data = {
            'id': id,
            'material': request.POST.get('material', linea.material),
            'estado': request.POST.get('estado', linea.estado),
            'diametro_pulg': request.POST.get('diametro_pulg', linea.diametro_pulg),
            'geom': geom,
        }
        result = LineasRiegoDJ().update(data)
        if not result.get('ok'):
            return JsonResponse({'ok': False, 'message': result.get('message'), 'data': []}, status=400)
        linea = LineasRiego.objects.get(id=id)
        return JsonResponse({'ok': True, 'message': 'Linea de riego actualizada', 'data': [model_to_wkt_dict(linea)]}, status=200)

    def delete(self, id):
        l = list(LineasRiego.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La linea de riego {id} no existe', 'data': []}, status=404)
        l[0].delete()
        return JsonResponse({'ok': True, 'message': f'Linea de riego {id} eliminada', 'data': []}, status=200)


class LineasRiegoModelViewSet(viewsets.ModelViewSet):
    """
    DRF ModelViewSet for LineasRiego.
    """
    queryset = LineasRiego.objects.all()
    serializer_class = LineasRiegoSerializer
    permission_classes = [permissions.AllowAny]

#  Plantas
class PlantasView(BaseDjangoView):
    def selectone(self, id):
        l = list(Plantas.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La planta {id} no existe', 'data': []}, status=404)
        planta = l[0]
        data = model_to_wkt_dict(planta)
        return JsonResponse({'ok': True, 'message': 'Planta recuperada', 'data': [data]}, status=200)

    def selectall(self):
        data = []
        for planta in Plantas.objects.all():
            data.append(model_to_wkt_dict(planta))
        return JsonResponse({'ok': True, 'message': 'Datos recuperados', 'data': data}, status=200)

    def insert(self, request):
        geom, error = get_required_wkt(request)
        if error:
            return error

        data = {
            'variedad': request.POST.get('variedad', ''),
            'estado_salud': request.POST.get('estado_salud', ''),
            'fecha_cosecha_est': request.POST.get('fecha_cosecha_est') or None,
            'geom': geom,
        }
        result = PlantasDJ().insert(data)
        if not result.get('ok'):
            return JsonResponse({'ok': False, 'message': result.get('message'), 'data': []}, status=400)
        planta = Plantas.objects.get(id=result['id'])
        return JsonResponse({'ok': True, 'message': 'Planta insertada', 'data': [model_to_wkt_dict(planta)]}, status=201)

    def update(self, request, id):
        l = list(Plantas.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La planta {id} no existe', 'data': []}, status=404)
        geom, error = get_required_wkt(request)
        if error:
            return error

        planta = l[0]
        data = {
            'id': id,
            'variedad': request.POST.get('variedad', planta.variedad),
            'estado_salud': request.POST.get('estado_salud', planta.estado_salud),
            'fecha_cosecha_est': request.POST.get('fecha_cosecha_est', planta.fecha_cosecha_est),
            'geom': geom,
        }
        result = PlantasDJ().update(data)
        if not result.get('ok'):
            return JsonResponse({'ok': False, 'message': result.get('message'), 'data': []}, status=400)
        planta = Plantas.objects.get(id=id)
        return JsonResponse({'ok': True, 'message': 'Planta actualizada', 'data': [model_to_wkt_dict(planta)]}, status=200)

    def delete(self, id):
        l = list(Plantas.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La planta {id} no existe', 'data': []}, status=404)
        l[0].delete()
        return JsonResponse({'ok': True, 'message': f'Planta {id} eliminada', 'data': []}, status=200)


class PlantasModelViewSet(viewsets.ModelViewSet):
    """
    DRF ModelViewSet for Plantas.
    """
    queryset = Plantas.objects.all()
    serializer_class = PlantasSerializer
    permission_classes = [permissions.AllowAny]
