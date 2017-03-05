import urllib2,contextlib
import datetime
from datetime import datetime
from collections import OrderedDict

from pytz import timezone
import gtfs_realtime_pb2
import google.protobuf
import copy
import vehicle,alert,tripupdate

import urllib,urllib2
import sys

class mtaUpdates5(object):

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
        start_time = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        timestamp = (timestamp - start_time).total_seconds() / 60
        dayOfWeek = datetime.datetime.today().weekday()
        if (int(dayOfWeek) >= 5):
            dayOfWeek = weekend
        else:
            dayOfWeek = weekday
        nytime = datetime.fromtimestamp(timestamp,self.TIMEZONE)


        for entity in feed.entity:
        # Trip update represents a change in timetable
            if entity.HasField('trip_update'):
                tmp = []
                #self.tripUpdates.append([])
                update = tripupdate.tripupdate()
                tmp.append(entity.trip_update.trip.trip_id)
                tmp.append(entity.trip_update.trip.route_id)
                tmp.append(timestamp)
                tmp.append(dayOfWeek)
                tmp.append(-1)
                tmp.append(-1)
                # find 96th and 42th street
                find = 0
                for stop in entity.trip_update.stop_time_update:
                    if (stop.stop_id == '120S' or stop.stop_id == '120N'):
                        find = find + 1
                        tmp[4] = (stop.arrival.time)
                    if (stop.stop_id == '631S' or stop.stop_id == '631N'):
                        find = find + 1
                        tmp[5] = (stop.arrival.time)
                if (find < 2):
                    continue
                self.tripUpdates.append(tmp)

            if entity.HasField('vehicle'):
                if (entity.vehicle.stop_id == '631S' or entity.vehicle.stop_id == '631N'):
                    self.tripUpdates[len(self.tripUpdates)-1][5] = entity.vehicle.timestamp

            #### INSERT ALERT CODE HERE #####

        
        return self.tripUpdates
    

