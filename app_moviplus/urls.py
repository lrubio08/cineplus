from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('resultado_busqueda/', views.resultado_busqueda, name= "resultado_busqueda" ),
    path('registro/', views.registro, name= "registro" ),
    path('registro_exitoso/', views.registro_exitoso, name= "registro_exitoso" ),
    path('iniciar_sesion/', views.iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('sala_privada/', views.sala_privada, name="sala_privada"),
    path('pelicula_seleccionada/<int:pelicula_id>/', views.pelicula_seleccionada, name='pelicula_seleccionada'),
    path('actor/', views.actor, name='actor'),
    path('actor_busquado/', views.actor_buscado, name = 'actor_buscado'),
    path('actor_buscado/<int:actor_id>/', views.actor_buscado, name='actor_buscado_by_id'),
    path('pelicula_actor/<int:actor_id>/', views.pelicula_actor, name = 'pelicula_actor'),
    path('reparto/<int:pelicula_id>/', views.ver_reparto, name='ver_reparto'),
]