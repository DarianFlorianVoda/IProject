import numpy as np
import pandas as pd
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


longitude = []
latitude = []


def findGeocode(city):
    try:
        geolocator = Nominatim(user_agent="your_app_name")
        return geolocator.geocode(city)
    except GeocoderTimedOut:
        return findGeocode(city)


def execGeocode():
    data = pd.read_csv('../Covid19Stats.csv')
    for i in data['Country']:
        if findGeocode(i) is not None:
            loc = findGeocode(i)
            latitude.append(loc.latitude)
            longitude.append(loc.longitude)
        else:
            latitude.append(np.nan)
            longitude.append(np.nan)
    print(latitude)
    print(longitude)

def checkGeocode():
    k = 0
    for j in range(len(latitude)):
        geolocator = Nominatim(user_agent="your_app_name")
        print(latitude[j], longitude[k])
        location = geolocator.reverse(str(str(latitude[k]) + ', ' + str(longitude[j])))
        print(location.address)
        k = k + 1