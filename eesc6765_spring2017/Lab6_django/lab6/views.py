from django.shortcuts import render

#TODO just for test
import random
import time
import thread
import sys
import json


TEMP = '0 Degrees Celsius'
daemonStart = False
TEMP_ARR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def getTemp():
	global TEMP, daemonStart
	while (True):
		daemonStart = True
		TEMP = str(random.randint(10,30))
		time.sleep(0.5)

# Create your views here.
def index(request):
	global TEMP, daemonStart, TEMP_ARR
	if (daemonStart == False):
		thread.start_new_thread(getTemp, ())
	print TEMP
	tempStr = TEMP + ' Degrees Celsius'
	sys.stdout.flush()
	context = {'curTemp': tempStr}

	del TEMP_ARR[0]
	TEMP_ARR.append(TEMP)

	return render(request, 'lab6/index.html', {'context': context, 'temparr': json.dumps(TEMP_ARR)})