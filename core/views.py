from django.shortcuts import render, redirect
from .models import Pelicula
from .forms import PeliculaForm, CustomUserForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate
# Create your views here.
import smtplib
from pyfcm import FCMNotification
from rest_framework import viewsets
from .serializers import PeliculaSerializer
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
import json
from fcm_django.models import FCMDevice

@csrf_exempt
@require_http_methods(['POST'])
def guardar_token(request):
	body = request.body.decode('utf-8')
	bodyDict = json.loads(body)
	token = bodyDict['token']
	existe = FCMDevice.objects.filter(registration_id =token, active = True)
	if len(existe) > 0:
		return HttpResponseBadRequest(json.dumps({'mensaje':'el token ya existe'}))

	dispositivo = FCMDevice()
	dispositivo.registration_id = token
	dispositivo.active = True

	if request.user.is_authenticated:
		dispositivo.user = request.user

	try:
		dispositivo.save()
		return HttpResponse(json.dumps({'mensaje': 'token guardado'}))
	except:
		return HttpResponseBadRequest(json.dumps({'mensaje': 'no se ha podido guardar'}))



def home(request):
	data = {
		'peliculas': Pelicula.objects.all()
	}
	return render(request, 'core/home.html', data)

def galeria(request):
	return render(request, 'core/galeria.html')	

def listado_pelicula(request):
	peliculas = Pelicula.objects.all()
	data = {
		'peliculas': peliculas
	}
	return render(request,'core/listado_peliculas.html', data)

@permission_required('core.add_pelicula')
def nueva_pelicula(request):
	data ={
		'form': PeliculaForm()
	}

	if request.method == 'POST':
		formulario = PeliculaForm(request.POST, files = request.FILES)
		if formulario.is_valid():
			formulario.save()

			#primero obtenemos todos los dispositivos
			dispositivos = FCMDevice.objects.filter(active = True)
			dispositivos.send_message(
				title = "Pelicula agregada",
				body = "Se ha agregado " + formulario.cleaned_data['nombre'],
				icon = "static/core/img/logo.png",
			)
			data['mensaje'] = 'Guardo correctamente'
		data['form'] = formulario
	return render(request, 'core/nueva_pelicula.html', data)

def modificar_pelicula(request, id):
	pelicula = Pelicula.objects.get(id = id)
	data ={
			'form': PeliculaForm(instance = pelicula)
	}	
	if request.method == 'POST':
		formulario = PeliculaForm(data = request.POST, instance = pelicula, files = request.FILES)
		if formulario.is_valid():
			formulario.save()
			data['mensaje'] = 'Modificado correctamente'
		data['form'] =  PeliculaForm(instance = Pelicula.objects.get(id = id))

	return render(request, 'core/modificar_pelicula.html', data)

def eliminar_pelicula(request,id):
	pelicula = Pelicula.objects.get(id = id)
	pelicula.delete()
	return redirect(to = 'listado_peliculas')

def registro_usuario(request):
	data = {
		'form': CustomUserForm()
	}
	if request.method == 'POST':
		formulario = CustomUserForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			#autenticar al usuario y redirigirlo al inicio
			username = formulario.cleaned_data['username']
			password = formulario.cleaned_data['password1']
			user = authenticate(username = username, password = password)
			login(request, user)
			return redirect(to=home)

	return render(request, 'registration/registrar.html', data)

class PeliculaViewSet(viewsets.ModelViewSet):
	queryset = Pelicula.objects.all()
	serializer_class = PeliculaSerializer