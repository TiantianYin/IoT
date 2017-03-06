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
import tripupdate,vehicle,alert,mtaUpdates5,aws

### YOUR CODE HERE ####

dynamodb = aws.getResource('dynamodb', 'us-east-1')


try:

  table = dynamodb.create_table(
    TableName='Lab5_new',
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
  table = dynamodb.Table('Lab5_new')
        #add function

#=====
#threads

#import threading

with open('key.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()
#newUpdate = mtaUpdates.mtaUpdates()

def add():
    while (True):
        #print 'Adding!'
        newUpdate = mtaUpdates5.mtaUpdates5(APIKEY)
        tr = newUpdate.getTripUpdates()
        #print "get done"
        if (len(tr) > 0):
            #print "tr is not None"
            for entity in tr:
   	        response = table.put_item(
     	            Item={
          	        'tripId': entity[0],
          	        'routeId': entity[1],
          	        'timestamp':entity[2],
                        'dayOfWeek':entity[3],
                        'timeAt96':entity[4],
                        'timeAt42':entity[5]
      	            }
    	        )
           # print "put item done"
        time.sleep(10)
        #print "waiting..."
        sys.stdout.flush()

def task2():
  time.sleep(20)
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
  time.sleep(40)


if __name__ == '__main__':
  #threads = []
  thread1 = Thread(target = add)
  thread1.setDaemon(True)
  #thread2 = Thread(target = task2)
  #thread2.setDaemon(True)
  thread1.start()
  #thread2.start()
  #threads.append(thread1)
  #threads.append(thread2)

  try:
    while(True):
      time.sleep(1)

  except KeyboardInterrupt:
    exit()
    print "Exit! But Daemon Remains!"

