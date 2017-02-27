# *********************************************************************************************
# Usage python mta.py

import json,time,csv,sys

import boto3
from boto3.dynamodb.conditions import Key,Attr

sys.path.append('../utils')
import aws


DYNAMODB_TABLE_NAME = "mtaData"

dynamodb = aws.getResource('dynamodb', 'us-east-1')

table = dynamodb.Table(DYNAMODB_TABLE_NAME)


# prompt
def prompt():
	print ""
	print ">Available Commands are : "
	print "1. plan trip"
	print "2. subscribe to messages"
	print "3. exit"  

tripID1 = '103100_4..N34R'
routeId1 = '4'

def main():
	prompt()
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





if __name__ == "__main__":
    main()
    

   

        
