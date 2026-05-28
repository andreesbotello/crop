from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'parcelas',    views.ParcelasModelViewSet, basename='parcelas')
router.register(r'lineasriego', views.LineasRiegoModelViewSet, basename='lineasriego')
router.register(r'plantas',     views.PlantasModelViewSet, basename='plantas')

urlpatterns = [
    path('hello_world/', views.HelloWorld.as_view(), name='crop_hello_world'),
    path('', include(router.urls)),
    path('not_loggedin/', views.notLoggedIn, name='crop_not_loggedin'),
    path('login/', views.LoginView.as_view(), name='crop_login'),
    path('logout/', views.LogoutView.as_view(), name='crop_logout'),
    path('isloggedin/', views.IsLoggedIn.as_view(), name='crop_isloggedin'),


    # CRUD manual para Parcelas (mismo patrón que buildings_view)
    # GET  /crop/parcelas_view/<action>/        → selectall
    # GET  /crop/parcelas_view/<action>/<id>/   → selectone
    # POST /crop/parcelas_view/insert/          → insert
    # POST /crop/parcelas_view/update/<id>/     → update
    # POST /crop/parcelas_view/delete/<id>/     → delete
    path('parcelas_view/<str:action>/',        views.ParcelasView.as_view(), name='parcelas_view'),
    path('parcelas_view/<str:action>/<int:id>/', views.ParcelasView.as_view(), name='parcelas_view_id'),
    path('lineasriego_view/<str:action>/',        views.LineasRiegoView.as_view(), name='lineasriego_view'),
    path('lineasriego_view/<str:action>/<int:id>/', views.LineasRiegoView.as_view(), name='lineasriego_view_id'),
    path('plantas_view/<str:action>/',        views.PlantasView.as_view(), name='plantas_view'),
    path('plantas_view/<str:action>/<int:id>/', views.PlantasView.as_view(), name='plantas_view_id'),
]
