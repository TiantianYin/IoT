from django.shortcuts import render
from django.http import JsonResponse
#from django import forms

from .forms import SrcForm
from .forms import DesForm

import sys
import json




# Create your views here.
def index(request):

	if request.method == 'POST':
		print request.POST.get('srcCity')
		print request.POST.get('desCity')
		sys.stdout.flush()

		srcWeather = ['17', 'Mostly Cloudy', '88']
		desWeather = ['17', 'Mostly Cloudy', '88']
		weather = [srcWeather, desWeather]
		return JsonResponse(json.dumps(weather), safe=False)
	else:
		srcForm = SrcForm()
		desForm = DesForm()
		return render(request, 'lab6/index.html', {'srcForm': srcForm, 'desForm': desForm})