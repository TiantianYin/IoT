#import requests

#url = "http://weather.yahooapis.com/forecastrss?w=26804118&u=c"
#response = requests.get(url)
#print response.content
import pprint
import pywapi

result = pywapi.get_weather_from_weather_com('BRXX0079', 'metric')
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(result)