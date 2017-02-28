# *********************************************************************************************
# Usage python mta.py

import json,time,csv,sys

import boto3
from boto3.dynamodb.conditions import Key,Attr
import boto.sns
import logging

sys.path.append('../utils')
import aws


DYNAMODB_TABLE_NAME = "mtaData"

dynamodb = aws.getResource('dynamodb', 'us-east-1')

table = dynamodb.Table(DYNAMODB_TABLE_NAME)

client = boto3.client('sns', 'us-east-1')

# prompt
def prompt():
	print ""
	print ">Available Commands are : "
	print "1. plan trip"
	print "2. subscribe to messages"
	print "3. exit"  

tripID1 = '103100_4..N34R'
routeId1 = '4'

def getTrain(stationID):
	routeId = dict()
	response = table.scan()
	local = []
  	express = []

  	for i in response['Items']:
  		try:
  			tmp = routeId[i['routeId']]
  		except KeyError:
  			for [k,v] in  i['futureStopData'].items():
  				k = str(k)
  				if len(k) >= 3:
  					if k[0:3] == stationID[0:3]:
  					#if k[0:3] == '120':
  						routeId[i['routeId']] = 1
  						break

  	for (k,v) in routeId.items():
  		if k == '1' or k == '6':
  			local.append(k)
  		else:
  			express.append(k)
  	print "Local:"
  	for i in local:
  		print i
  	print "Express:"
  	for i in express:
  		print i
  	return [local,express]


def getEarliest(stopID, timestamp):
	response = table.scan()
	trains = getTrain(stopID)
	localTimeToArrive = 9999999999
	expressTimeToArrive = 9999999999
	localTripId = "-1"
	expressTripId = "-1"
  	for i in response['Items']:
  		if (i['routeId'] in trains[0]) or (i['routeId'] in trains[1]):
  			for [k,v] in  i['futureStopData'].items():
  				if k == stopID:
  					for j in v:
  						try:
  							arrTime = j['arrivaltime']
  							arrTime = long(arrTime)
  							timeToArrive = arrTime - timestamp
  							if i['routeId'] in trains[0]:
  								if timeToArrive >= 0 and timeToArrive < localTimeToArrive:
  									localTimeToArrive = arrTime
  									localTripId = i['tripId']
  							else:
  								if timeToArrive >= 0 and timeToArrive < expressTimeToArrive:
  									expressTimeToArrive = arrTime
  									expressTripId = i['tripId']
  						except KeyError:
  							continue
  	return [localTimeToArrive, expressTimeToArrive, localTripId, expressTripId]


def getTime(start, destination, timestamp):
	response = table.scan()
	#trains = getTrain(stationID)
	#if the start station is north than 96 (120), and heading to the south: 
	#startTrain = getEarliest(stationID, timestamp)
	#startID = '117'
	nextTimeArrive = 9999999999
	idOfTrain = 1
	localTripId = None

	#get the next train in start station 
	for i in response['Items']:
		if i['routeId'] == '1' :
			try:
				nex_time = i['futureStopData'][start + 'S'][0]['arrivaltime']
				if nex_time >= timestamp and nex_time < nextTimeArrive :
					nextTimeArrive = nex_time
					idOfTrain = 1
					localTripId = i['tripId']
			except KeyError:
				continue

	#here we get the start time and the train
	timeTo96 = timeTo(localTripId, '120', 'S')
	timeTo42 = timeTo(localTripId, '127', 'S')
	print timeTo96
	print timeTo42

	expTripId = getEarliest('120S', timeTo96)[3]   #get the tripId from 96 express train
	print expTripId
	#timeTo42Exp = timeTo(expTripId, '127', 'S')


	#return [timeTo42, timeTo42Exp]

def sendPlan(start, destination, timestamp):
	msg = " "
	"""
	twoTimes = getTime(start, destination, timestamp)
	if twoTimes[0] <= twoTimes[1]:
		msg = "Stay"
	else:
		msg = "Switch"
	"""
	#----
	k = getEarliest(str(start) + 'S', time.time())
	msg = k[2]
	#----
	print msg
	response = client.publish(
		TopicArn='arn:aws:sns:us-east-1:768104751743:IoT_Lab4_1',
		Message=msg
	)


#reply when subscribe
def replyToNew():
	while True:
		phone_num = raw_input('Please input your phone number: ')
		if phone_num.isdigit():
			break
		else:
			print 'Illegal Input! Please input again.'


	new_arn = client.subscribe(
		TopicArn='arn:aws:sns:us-east-1:768104751743:IoT_Lab4_1',
		Protocol='sms',
		Endpoint=phone_num
	)

	msg = "Subscribe Success!"

	response = client.publish(
    	PhoneNumber=phone_num,
    	Message=msg
	)


def main():
	#print getTrain('120')
	#print getEarliest('120S', time.time())
	try:
		while True:
			while True:
				prompt()
				choose=raw_input('Please input your choice:')
				if choose == '1' or choose == '2' or choose == '3':
					break
				else:
					print 'Illegal input! Please input again.'
			if choose == '1':
				print '!'
				print 'Please input your start startID and destinationID:'
				while True:
					startID=raw_input('StationID: ')
					destinationID=raw_input('DestinationID: ')
					#TODO check stationID
					break
				sendPlan(str(startID), str(destinationID), time.time())
			elif choose == '2':
				replyToNew()
			else:
				print 'Thanks for using!'
				exit()
	except KeyboardInterrupt:
		exit()



"""
	response = table.scan(
		#KeyConditionExpression=Key('year').eq(1985)
		FilterExpression = Key('startDate').between('20170220', '20170222')
		#FilterExpression = Key('startDate').eq(20170221)
	)
	result=table.delete_item( 
		Key={
			'tripId': tripID1,
			'routeId': routeId1
		}
	)


  	for i in response['Items']:
		result=table.delete_item( 
			Key={
				'tripId': i['tripId'],
				'routeId': i['routeId']
			}
		)

	return 0
"""


if __name__ == "__main__":
    main()
    

   

        
