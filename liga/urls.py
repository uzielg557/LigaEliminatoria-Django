from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_principal, name='panel_principal'),

    path('equipos/', views.listar_equipos, name='listar_equipos'),
    path('equipos/crear/', views.crear_equipo, name='crear_equipo'),
    path('equipos/editar/<int:id>/', views.editar_equipo, name='editar_equipo'),
    path('equipos/eliminar/<int:id>/', views.eliminar_equipo, name='eliminar_equipo'),

    path('generar-jornadas/', views.generar_jornadas, name='generar_jornadas'),
    path('registrar-resultados/', views.registrar_resultados, name='registrar_resultados'),
    path('tabla/', views.tabla_posiciones, name='tabla_posiciones'),
    path('eliminatorias/', views.elegir_eliminatoria, name='elegir_eliminatoria'),
    path("eliminatorias/generar/<int:cantidad>/", views.generar_eliminatoria, name="generar_eliminatoria"),
    path("eliminatorias/registrar/", views.registrar_eliminatoria, name="registrar_eliminatoria"),
]