from django.shortcuts import render
from django.http import JsonResponse
#from django import forms

from .forms import SrcForm
from .forms import DesForm

import sys
import json

import pywapi


def getWeather(city):
	id = pywapi.get_loc_id_from_weather_com(city)
	result = pywapi.get_weather_from_weather_com(id[0][0], 'metric')
	cur = result['current_conditions']
	res = [city, cur['temperature'], cur['text'], cur['visibility']]
	return res

# Create your views here.
def index(request):

	if request.method == 'POST':
		srcCity = request.POST.get('srcCity')
		desCity = request.POST.get('desCity')
		print srcCity
		print desCity
		sys.stdout.flush()

		srcWeather = getWeather(srcCity)
		desWeather = getWeather(desCity)
		weather = [srcWeather, desWeather]
		return JsonResponse(json.dumps(weather), safe=False)
	else:
		srcForm = SrcForm()
		desForm = DesForm()
		return render(request, 'lab6/index.html', {'srcForm': srcForm, 'desForm': desForm})