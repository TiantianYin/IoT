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

"""
def getTrain(stationID):
def getEarliest(stationID, timestamp):
def getTime(start, destination, timestamp):
def sendPlan(start, destination, timestamp):
"""

#reply when subscribe
def replyToNew():
	while True:
		phone_num = raw_input('Please input your phone number:')
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
    	TopicArn='arn:aws:sns:us-east-1:768104751743:IoT_Lab4_1',
    	TargetArn=new_arn
    	Message=msg
	)


def main():
	while True:
		prompt()
		choose=raw_input('Please input your choice:')
		if choose == '1' or choose == '2' or choose == '3':
			break
		else:
			print 'Illegal Input! Please input again.'
	if choose == '1':
	elif choose == '2':
		replyToNew()
	else:
		exit





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
    

   

        
