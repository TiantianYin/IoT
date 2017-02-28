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
    currentStopId = "-1"
    currentStopStatus = -1
    vehicleTimeStamp = -1
    futureStopData = OrderedDict()
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
        # Trip update represents a change in timetable
            if entity.HasField('trip_update'):
                newItem = awsItem()
                newItem.timeStamp = timestamp

                newItem.tripId = entity.trip_update.trip.trip_id
                newItem.routeId = entity.trip_update.trip.route_id
                newItem.startDate = entity.trip_update.trip.start_date
                newItem.direction = entity.trip_update.stop_time_update[0].stop_id[-1]
                for stop in entity.trip_update.stop_time_update:
                    newItem.futureStopData[stop.stop_id] = [{'arrivaltime': stop.arrival.time or None}, {'departuretime': stop.departure.time or None}]
                self.tripUpdates.append(newItem)

            if entity.HasField('vehicle'):
                self.tripUpdates[len(self.tripUpdates)-1].currentStopId = entity.vehicle.stop_id
                #print "$$$$$$$$$$" +newItem.currentStopId+ "$$$$$$$$$$"
                self.tripUpdates[len(self.tripUpdates)-1].vehicleTimeStamp = entity.vehicle.timestamp
                #print "!!!!!!!!!!" +str(newItem.vehicleTimeStamp)+ "!!!!!!!!!!"
                self.tripUpdates[len(self.tripUpdates)-1].currentStopStatus = entity.vehicle.current_status
                #print "**********" +str(newItem.currentStopStatus)+ "**********"

            if entity.HasField('alert'):
                a = alert.alert()
                a.alertMessage = entity.alert.header_text.translation
                #a.alertMessage = entity.alert.header_text.translation.text
                self.alerts.append(a)

            #### INSERT ALERT CODE HERE #####

        
        return self.tripUpdates
    
    # END OF getTripUpdates method

if __name__ == '__main__':
    apikey = '7b0c2537b0f7349b92499a8387da47bd'
    mta = mtaUpdates(apikey)
    res = mta.getTripUpdates()
    print res
