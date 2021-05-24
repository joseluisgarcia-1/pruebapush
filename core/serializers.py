# que es un serializador en django

from rest_framework import serializers 
from .models import Pelicula

class PeliculaSerializer(serializers.ModelSerializer):
	"""docstring for PeliculaSerializer"""
	class Meta:
		model = Pelicula
		fields = ['nombre', 'duracion', 'anio', 'sinopsis', 'fecha_estreno','genero']
