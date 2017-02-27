import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict

from pytz import timezone
import gtfs_realtime_pb2
import google.protobuf

import vehicle,alert,tripupdate

import urllib,urllib2
import sys


class awsItem(object):
    tripId = None
    routeId = None
    startDate = None
    direction = None
    currentStopId = None
    currentStopStatus = None
    vehicleTimeStamp = None
    futureStopData = None
    timeStamp = None

class mtaUpdates(object):

    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')
    
    # feed url depends on the routes to which you want updates
    # here we are using feed 1 , which has lines 1,2,3,4,5,6,S
    # While initializing we can read the API Key and add it to the url
    feedurl = 'http://datamine.mta.info/mta_esi.php?feed_id=1&key='
    
    VCS = {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"}    
    tripUpdates = []
    alerts = []

    def __init__(self,apikey):
        self.feedurl = self.feedurl + apikey

    # Method to get trip updates from mta real time feed
    def getTripUpdates(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            with contextlib.closing(urllib2.urlopen(self.feedurl)) as response:
                d = feed.ParseFromString(response.read())
        except (urllib2.URLError, google.protobuf.message.DecodeError) as e:
            print "Error while connecting to mta server " +str(e)
    
        timestamp = feed.header.timestamp
        nytime = datetime.fromtimestamp(timestamp,self.TIMEZONE)
        

        for entity in feed.entity:
            newItem = awsItem()
            newItem.timeStamp = timestamp
        # Trip update represents a change in timetable
            if entity.trip_update and entity.trip_update.trip.trip_id:
                update = tripupdate.tripupdate()

                newItem.tripId = entity.trip_update.trip.trip_id
                newItem.routeId = entity.trip_update.trip.route_id
                newItem.startDate = entity.trip_update.trip.start_date
                newItem.direction = None
                stopId = None

                newItem.futureStopData = str(entity.trip_update.stop_time_update)
                #print  newItem.futureStopData


                #for stop_time_update in entity.trip_update:
                for stop_time_update in []:
                    arrivalTime = None
                    departureTime = None
                    if stop_time_update.arrival:
                        arrivalTime = stop_time_update.arrival.time
                    if stop_time_update.departure:
                        departureTime = stop_time_update.departure.time

                    update.futureStops[stopId] = [{"arrivalTime":arrivalTime}, {"departureTime": departureTime}]

                for i in newItem.tripId:
                    if i == 'N':
                        stopId = 'N'
                        break;
                    if i == 'S':
                        stopId = 'S'

                newItem.direction = stopId

                update.tripId = newItem.tripId
                update.routeId = newItem.routeId
                update.startDate = newItem.startDate
                update.direction = newItem.direction


                #self.tripUpdates.append(update)



            ##### INSERT TRIPUPDATE CODE HERE ####  

            if entity.vehicle and entity.vehicle.trip.trip_id:
                v = vehicle.vehicle()

                
                newItem.currentStopId = entity.vehicle.stop_id
                newItem.vehicleTimeStamp = entity.vehicle.timestamp
                newItem.currentStopStatus = entity.vehicle.current_status

                v.currentStopNumber = entity.vehicle.current_stop_sequence
                v.currentStopId = newItem.currentStopId
                v.timestamp = newItem.vehicleTimeStamp
                v.currentStopStatus = newItem.currentStopStatus
                
                #self.vehicles.append(v)

            ##### INSERT VEHICLE CODE HERE #####
            
            if entity.alert:
                a = alert.alert()
                a.alertMessage = entity.alert.header_text.translation
                #a.alertMessage = entity.alert.header_text.translation.text
                self.alerts.append(a)

            #### INSERT ALERT CODE HERE #####
            if newItem.tripId:
                self.tripUpdates.append(newItem)

        
        return self.tripUpdates
    
    # END OF getTripUpdates method


