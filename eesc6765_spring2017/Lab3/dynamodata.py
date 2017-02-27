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
 
 newUpdate = mtaUpdates.mtaUpdates(APIKEY)
 tr = newUpdate.getTripUpdates()
 for entity in tr:
  #print "$$$$$$$$$$" +entity.currentStopId+ "$$$$$$$$$$"
  #print "!!!!!!!!!!" +str(entity.vehicleTimeStamp)+ "!!!!!!!!!!"
  #print "**********" +str(entity.currentStopStatus)+ "**********"
 	response = table.put_item(
   		Item={
        	'tripId': entity.tripId,
        	'routeId': entity.routeId,
        	'startDate':entity.startDate,
        	'direction':entity.direction,
        	'currentStopId':str(entity.currentStopId),
        	'currentStopStatus':str(entity.currentStopStatus),
        	'vehicleTimeStamp': str(entity.vehicleTimeStamp),
        	'futureStopData':entity.futureStopData,
        	'timeStamp':entity.timeStamp
    	     }
  	)


 #add to AWS
 return

"""
def task1():
 #View all data from
 #check and delete
 response = table.query(
     KeyConditionExpression=Key('timeStamp').between('0', '1000')
)
 return
"""
def task2():
 #View all data from
 #check and delete
	response = table.query(
    		#KeyConditionExpression=Key('year').eq(1985)
    		KeyConditionExpression = Key('startDate').between(20170220, 20170222)
  	)

  	for i in response['Items']:
    		table.delete_item(tripId=i['tripId'])



def worker(num):
    """thread worker function"""
    print 'Worker: %s' % num
    try:
     while (1):
      if num == 0:
       task1()
       time.sleep(30)
      else:
       task2();
       time.sleep(60)

    except KeyboardInterrupt:
      exit
    return


threads = []
for i in range(1):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()