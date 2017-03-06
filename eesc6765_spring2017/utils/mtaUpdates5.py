import urllib2,contextlib
import datetime
#from datetime import datetime
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
    stopAt42 = ["127S", "631S", "723S", "725S", "901S", "902S", "A27S", "D16S",  "R16S",]

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
    
        print "timestamp = " + str(feed.header.timestamp)
        ts = datetime.datetime.fromtimestamp(int(feed.header.timestamp), self.TIMEZONE)
        ts = ts.replace(tzinfo=None)
        #timestamp = datetime.datetime.fromtimestamp(int(nytime))

        start_time = ts.replace(hour=0, minute=0, second=0, microsecond=0)

        #start_time = datetime.datetime(year, month, day, tzinfo=self.TIMEZONE) 
        print "start_time = " + start_time.strftime("%Y-%m-%d %H:%M");
        print "cur_time = " + ts.strftime("%Y-%m-%d %H:%M");
        timestamp = int((ts - start_time).total_seconds() / 60)
        dayOfWeek = ts.weekday()
        print "minutes = " + str(timestamp)
        print "dayOfWeek = " + str(dayOfWeek)
        if (int(dayOfWeek) >= 5):
            dayOfWeek = "weekend"
        else:
            dayOfWeek = "weekday"


        for entity in feed.entity:
        # Trip update represents a change in timetable
            if entity.HasField('trip_update'):
                tmp = []
                #self.tripUpdates.append([])
                find = 0
                update = tripupdate.tripupdate()
                tmp.append(entity.trip_update.trip.trip_id)
                route_id = entity.trip_update.trip.route_id
                try:
                    route_id = int(route_id)
                except ValueError:
                    continue
                if (route_id > 3):
                    continue
                tmp.append(entity.trip_update.trip.route_id)
                tmp.append(timestamp)
                tmp.append(dayOfWeek)
                tmp.append(-1)
                tmp.append(-1)
                # find 96th and 42th street
                for stop in entity.trip_update.stop_time_update:
                    if (stop.stop_id == '120S'):
                        find = find + 1 
                        stamp = datetime.datetime.fromtimestamp(int(stop.arrival.time))
                        t = int((stamp - start_time).total_seconds() / 60)
                        tmp[4] = (t)
                    if (stop.stop_id in self.stopAt42):
                        find = find + 1
                        stamp = datetime.datetime.fromtimestamp(int(stop.arrival.time))
                        t = int((stamp - start_time).total_seconds() / 60)
                        tmp[5] = (t)

                print "entity = " + entity.id + " find = " + str(find)
                if (find < 2):
                    continue
                self.tripUpdates.append(tmp)

            if entity.HasField('vehicle'):
                if ((entity.vehicle.stop_id in self.stopAt42) and (find == 2)):
                    stamp = datetime.datetime.fromtimestamp(int(entity.vehicle.timestamp))
                    t = int((stamp - start_time).total_seconds() / 60)
                    self.tripUpdates[len(self.tripUpdates)-1][5] = t

            #### INSERT ALERT CODE HERE #####

        
        return self.tripUpdates
    

