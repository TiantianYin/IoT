#import requests

#url = "http://weather.yahooapis.com/forecastrss?w=26804118&u=c"
#response = requests.get(url)
#print response.content
import pprint
import pywapi
id = pywapi.get_loc_id_from_weather_com("oklahoma city, ok")
print id

result = pywapi.get_weather_from_weather_com(id[0][0], 'metric')
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(result)