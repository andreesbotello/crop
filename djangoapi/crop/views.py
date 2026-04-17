# Django imports
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin

# rest_framework imports
from rest_framework import viewsets, permissions

# My imports
from crop.models import Parcelas, LineasRiego, Plantas
from crop.serializers import ParcelasSerializer, LineasRiegoSerializer, PlantasSerializer
from core.myLib.baseDjangoView import BaseDjangoView


class HelloWorld(View):
    def get(self, request):
        return JsonResponse({"ok": True, "message": "Crop. Hello world", "data": []})


# ─────────────────────────────────────────────
#  Parcelas
# ─────────────────────────────────────────────

class ParcelasView(LoginRequiredMixin, BaseDjangoView):
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
        return JsonResponse({'ok': True, 'message': 'Parcela recuperada', 'data': [model_to_dict(l[0])]}, status=200)

    def selectall(self):
        data = [model_to_dict(p) for p in Parcelas.objects.all()]
        return JsonResponse({'ok': True, 'message': 'Datos recuperados', 'data': data}, status=200)

    def insert(self, request):
        dueno    = request.POST.get('dueno', '')
        cultivo  = request.POST.get('cultivo', '')
        p = Parcelas(dueno=dueno, cultivo=cultivo)
        p.save()
        return JsonResponse({'ok': True, 'message': 'Parcela insertada', 'data': [model_to_dict(p)]}, status=201)

    def update(self, request, id):
        l = list(Parcelas.objects.filter(id=id))
        if not l:
            return JsonResponse({'ok': False, 'message': f'La parcela {id} no existe', 'data': []}, status=404)
        p = l[0]
        p.dueno   = request.POST.get('dueno', p.dueno)
        p.cultivo = request.POST.get('cultivo', p.cultivo)
        p.save()
        return JsonResponse({'ok': True, 'message': 'Parcela actualizada', 'data': [model_to_dict(p)]}, status=200)

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


# ─────────────────────────────────────────────
#  Líneas de riego
# ─────────────────────────────────────────────

class LineasRiegoModelViewSet(viewsets.ModelViewSet):
    """
    DRF ModelViewSet for LineasRiego.
    """
    queryset = LineasRiego.objects.all()
    serializer_class = LineasRiegoSerializer
    permission_classes = [permissions.AllowAny]


# ─────────────────────────────────────────────
#  Plantas
# ─────────────────────────────────────────────

class PlantasModelViewSet(viewsets.ModelViewSet):
    """
    DRF ModelViewSet for Plantas.
    """
    queryset = Plantas.objects.all()
    serializer_class = PlantasSerializer
    permission_classes = [permissions.AllowAny]
