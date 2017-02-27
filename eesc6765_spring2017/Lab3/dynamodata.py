# *********************************************************************************************
# Program to update dynamodb with latest data from mta feed. It also cleans up stale entried from db
# Usage python dynamodata.py
# *********************************************************************************************
#from __future__ import print_function # Python 2/3 compatibility
#import boto3
import json,time,sys
import threading
from collections import OrderedDict
from threading import Thread

import time

import boto3
from boto3.dynamodb.conditions import Key,Attr
#from __future__ import print_function # Python 2/3 compatibility
#import boto3

sys.path.append('../utils')
import tripupdate,vehicle,alert,mtaUpdates,aws

### YOUR CODE HERE ####

dynamodb = aws.getResource('dynamodb', 'us-east-1')


try:

  table = dynamodb.create_table(
    TableName='mtaData',
    KeySchema=[
        {
            'AttributeName': 'tripId',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'routeId',
            'KeyType': 'RANGE'  #Sort key
        }
    ],

    AttributeDefinitions=[
        {
            'AttributeName': 'tripId',
            'AttributeType': 'S'
        },
		{
            'AttributeName': 'routeId',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
  )
  print("Table status:", table.table_status)
except:
  table = dynamodb.Table('mtaData')
        #add function

#=====
#threads

#import threading

with open('key.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()
#newUpdate = mtaUpdates.mtaUpdates()

def task1():
  print 'Adding!'
  newUpdate = mtaUpdates.mtaUpdates(APIKEY)
  tr = newUpdate.getTripUpdates()
  for entity in tr:
   	response = table.put_item(
     		Item={
          	'tripId': entity.tripId,
          	'routeId': entity.routeId,
          	'startDate':entity.startDate,
          	'direction':entity.direction,
          	'currentStopId':entity.currentStopId,
          	'currentStopStatus':entity.currentStopStatus,
          	'vehicleTimeStamp':entity.vehicleTimeStamp,
          	'futureStopData':entity.futureStopData,
          	'timeStamp':entity.timeStamp
      	     }
    	)
  time.sleep(30)

def task2():
  print("Deleting!")
  min_time = int(time.time()) - 120
  response = table.scan(
    FilterExpression = Key('timeStamp').between(0, min_time)
  )

  for i in response['Items']:
    result=table.delete_item(
      Key={
        'tripId': i['tripId'],
        'routeId': i['routeId']
      }
    )
  time.sleep(60)


if __name__ == '__main__':
  threads = []
  thread1 = Thread(target = task1)
  thread1.setDaemon(True)
  thread2 = Thread(target = task2)
  thread2.setDaemon(True)
  thread1.start()
  thread2.start()
  threads.append(thread1)
  threads.append(thread2)

  try:
    while(True):
      time.sleep(0.5)
  except KeyboardInterrupt:
    for t in threads:
      t.join()
    print "Exit! But Daemon Remains!"

