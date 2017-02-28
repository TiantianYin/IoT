import boto.sns
import logging
import boto3
import mraa
import pyupm_i2clcd as lcd
import math

tempSensor = mraa.Aio(1)
temp = float (tempSensor.read())
temp = 1023.0/(temp)-1.0;
temp = 100000.0 * temp;
temp = 1.0/(math.log(temp/100000.0)/4275+1/298.15)-273.15

client = boto3.client('sns', 'us-east-1')

msg = "The current temprature is: " + str(temp)

print msg
response = client.publish(
    TopicArn='arn:aws:sns:us-east-1:768104751743:IoT_Lab4_1',
    #TargetArn='arn:aws:sns:us-east-1:768104751743:IoT_Lab4_1:1a93e108-c975-437e-bd2e-ef08a6bc69d9',
    Message=msg
)
