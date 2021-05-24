from django.urls import path, include
from .views import home, galeria,listado_pelicula, nueva_pelicula, modificar_pelicula, eliminar_pelicula, registro_usuario, PeliculaViewSet, guardar_token
from rest_framework import routers

router = routers.DefaultRouter()
router.register('peliculas', PeliculaViewSet)
urlpatterns = [
    path('', home, name = 'home'),
    path('galeria/', galeria, name = 'galeria'),
	path('listado-pelicula/', listado_pelicula, name = 'listado_peliculas'),
	path('nueva-pelicula/', nueva_pelicula, name = 'nueva_peliculas'),
	path('modificar-pelicula/<id>/', modificar_pelicula, name = 'modificar_peliculas'),
	path('eliminar-pelicula/<id>/', eliminar_pelicula, name = 'eliminar_peliculas'),
	path('registro/', registro_usuario, name = 'registro_usuario'),
	path('api/', include(router.urls)),
	path('guardar-token/', guardar_token, name = 'guardar_token'),

]
 