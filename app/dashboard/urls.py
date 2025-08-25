# dashboard/urls.py - Archivo actualizado con nueva ruta

from django.urls import path
from . import views
from .views import ContratoListView, ContratoInteradministrativoListView

urlpatterns = [
    path('index/', views.index, name="index"),  # ESTA LÍNEA DEBE ESTAR PRIMERA
    path('dashboard/', views.dashboard, name="dashboard"),
    path('expired/', views.expired, name="expired"),
    path('expired-edur/', views.expirededur, name="expirededur"),
    path('report/', ContratoListView.as_view(), name='contratos_list'),
    path('api/', views.api, name="api"),
    path('api-interadmin/', views.api_interadministrativos, name="api_interadministrativos"),  # NUEVA RUTA
    path('emilia/', views.emilia, name="emilia"),
    path('contratos-interadministrativos/', ContratoInteradministrativoListView.as_view(), name='contratos_interadmin_list'),
]