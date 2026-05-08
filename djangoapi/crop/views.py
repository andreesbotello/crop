# Django imports
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import random
import time

from rest_framework import viewsets, permissions

from crop.models import Parcelas, LineasRiego, Plantas
from crop.serializers import ParcelasSerializer, LineasRiegoSerializer, PlantasSerializer
from core.myLib.baseDjangoView import BaseDjangoView

class HelloWorld(View):
    def get(self, request):
        return JsonResponse({"ok": True, "message": "Crop. Hello world", "data": []})

def notLoggedIn(request):
    return JsonResponse({"ok": False, "message": "You are not logged in", "data": []}, status=400)

class LoginView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            username = request.user.username
            return JsonResponse({
                "ok": True,
                "message": "The user {0} already is authenticated".format(username),
                "data": [{"username": username}],
            }, status=200)

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({
                "ok": True,
                "message": "User {0} logged in".format(username),
                "data": [{"username": username}],
            }, status=200)

        seconds = random.uniform(0, 1)
        time.sleep(seconds)
        return JsonResponse({"ok": False, "message": "Wrong user or password", "data": []}, status=400)

class LogoutView(LoginRequiredMixin, View):
    login_url = "/crop/not_loggedin/"

    def post(self, request, *args, **kwargs):
        username = request.user.username
        logout(request)
        return JsonResponse({
            "ok": True,
            "message": "The user {0} is now logged out".format(username),
            "data": [],
        }, status=200)

class IsLoggedIn(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return JsonResponse({
                "ok": True,
                "message": "You are authenticated",
                "data": [{"username": request.user.username}],
            }, status=200)

        return JsonResponse({"ok": False, "message": "You are not authenticated", "data": []}, status=400)

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
        p = l[0]
        data = model_to_dict(p)
        if data.get('geom'):
            data['geom'] = json.loads(p.geom.geojson)
        return JsonResponse({'ok': True, 'message': 'Parcela recuperada', 'data': [data]}, status=200)

    def selectall(self):
        data = []
        for p in Parcelas.objects.all():
            p_dict = model_to_dict(p)
            if p_dict.get('geom'):
                p_dict['geom'] = json.loads(p.geom.geojson)
            data.append(p_dict)
        return JsonResponse({'ok': True, 'message': 'Datos recuperados', 'data': data}, status=200)

    def insert(self, request):
        dueno    = request.POST.get('dueno', '')
        cultivo  = request.POST.get('cultivo', '')
        p = Parcelas(dueno=dueno, cultivo=cultivo)
        p.save()
        p_dict = model_to_dict(p)
        if p_dict.get('geom'):
            p_dict['geom'] = json.loads(p.geom.geojson)
        return JsonResponse({'ok': True, 'message': 'Parcela insertada', 'data': [p_dict]}, status=201)

    def update(self, request, id):
        l = list(Parcelas.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La parcela {id} no existe', 'data': []}, status=404)
        p = l[0]
        p.dueno   = request.POST.get('dueno', p.dueno)
        p.cultivo = request.POST.get('cultivo', p.cultivo)
        p.save()
        p_dict = model_to_dict(p)
        if p_dict.get('geom'):
            p_dict['geom'] = json.loads(p.geom.geojson)
        return JsonResponse({'ok': True, 'message': 'Parcela actualizada', 'data': [p_dict]}, status=200)

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
        data = model_to_dict(linea)
        if data.get('geom'):
            data['geom'] = json.loads(linea.geom.geojson)
        return JsonResponse({'ok': True, 'message': 'Linea de riego recuperada', 'data': [data]}, status=200)

    def selectall(self):
        data = []
        for linea in LineasRiego.objects.all():
            linea_dict = model_to_dict(linea)
            if linea_dict.get('geom'):
                linea_dict['geom'] = json.loads(linea.geom.geojson)
            data.append(linea_dict)
        return JsonResponse({'ok': True, 'message': 'Datos recuperados', 'data': data}, status=200)

    def insert(self, request):
        material = request.POST.get('material', '')
        estado = request.POST.get('estado', '')
        diametro_pulg = request.POST.get('diametro_pulg') or None
        longitud_m = request.POST.get('longitud_m') or None
        linea = LineasRiego(
            material=material,
            estado=estado,
            diametro_pulg=diametro_pulg,
            longitud_m=longitud_m,
        )
        linea.save()
        linea_dict = model_to_dict(linea)
        if linea_dict.get('geom'):
            linea_dict['geom'] = json.loads(linea.geom.geojson)
        return JsonResponse({'ok': True, 'message': 'Linea de riego insertada', 'data': [linea_dict]}, status=201)

    def update(self, request, id):
        l = list(LineasRiego.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La linea de riego {id} no existe', 'data': []}, status=404)
        linea = l[0]
        linea.material = request.POST.get('material', linea.material)
        linea.estado = request.POST.get('estado', linea.estado)
        linea.diametro_pulg = request.POST.get('diametro_pulg', linea.diametro_pulg)
        linea.longitud_m = request.POST.get('longitud_m', linea.longitud_m)
        linea.save()
        linea_dict = model_to_dict(linea)
        if linea_dict.get('geom'):
            linea_dict['geom'] = json.loads(linea.geom.geojson)
        return JsonResponse({'ok': True, 'message': 'Linea de riego actualizada', 'data': [linea_dict]}, status=200)

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
        data = model_to_dict(planta)
        if data.get('geom'):
            data['geom'] = json.loads(planta.geom.geojson)
        return JsonResponse({'ok': True, 'message': 'Planta recuperada', 'data': [data]}, status=200)

    def selectall(self):
        data = []
        for planta in Plantas.objects.all():
            planta_dict = model_to_dict(planta)
            if planta_dict.get('geom'):
                planta_dict['geom'] = json.loads(planta.geom.geojson)
            data.append(planta_dict)
        return JsonResponse({'ok': True, 'message': 'Datos recuperados', 'data': data}, status=200)

    def insert(self, request):
        variedad = request.POST.get('variedad', '')
        estado_salud = request.POST.get('estado_salud', '')
        fecha_cosecha_est = request.POST.get('fecha_cosecha_est') or None
        planta = Plantas(
            variedad=variedad,
            estado_salud=estado_salud,
            fecha_cosecha_est=fecha_cosecha_est,
        )
        planta.save()
        planta_dict = model_to_dict(planta)
        if planta_dict.get('geom'):
            planta_dict['geom'] = json.loads(planta.geom.geojson)
        return JsonResponse({'ok': True, 'message': 'Planta insertada', 'data': [planta_dict]}, status=201)

    def update(self, request, id):
        l = list(Plantas.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La planta {id} no existe', 'data': []}, status=404)
        planta = l[0]
        planta.variedad = request.POST.get('variedad', planta.variedad)
        planta.estado_salud = request.POST.get('estado_salud', planta.estado_salud)
        planta.fecha_cosecha_est = request.POST.get('fecha_cosecha_est', planta.fecha_cosecha_est)
        planta.save()
        planta_dict = model_to_dict(planta)
        if planta_dict.get('geom'):
            planta_dict['geom'] = json.loads(planta.geom.geojson)
        return JsonResponse({'ok': True, 'message': 'Planta actualizada', 'data': [planta_dict]}, status=200)

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
