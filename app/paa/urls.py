from django.urls import path
from . import views

app_name = 'paa'

urlpatterns = [
    path('', views.index, name='index'),
    path('generar/', views.generar_certificado, name='generar_certificado'),
]
