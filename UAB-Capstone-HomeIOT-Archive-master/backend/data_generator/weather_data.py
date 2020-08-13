#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 15:36:40 2019

@author: senaypatel
"""

from darksky import forecast
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import certifi
import ssl


"""
Make an instance of this
with two atributes city_name
and state_name.
place = Location(city_name,state_name)
"""
class City_location():
    def __init__(self, city_name:  str, state_name: str, key: str):
        self.city_name =city_name
        self.state_name = state_name
        self.key = key

    def do_geocode(self, place):
        try:
            geolocator = Nominatim(user_agent="darksky1")
            return geolocator.geocode(place)
        except GeocoderTimedOut:
            return self.do_geocode(place)
        
    """
    CAll this function to get
    latitude of a place
    """
    def latitude(self) -> float:
        place = self.city_name + " " + self.state_name
        locate = self.do_geocode(place)     
        return locate.latitude

    
    """
    CAll this function to get
    longitude of the place
    """
    def longitude(self) -> float:
        place = self.city_name + " " + self.state_name
        locate = self.do_geocode(place)    
        return locate.longitude

    
    """
    The data of a date will be generated hourly
    in dictionary where hours(1-24) are used as
    keys and temperature is value.
    """
    def one_day_temp(self, date):
        lat=  self.latitude()
        longi = self.longitude()
        PLACE = self.key, lat, longi
        yy = date.year
        mm = date.month
        dd = date.day
        hh = date.hour
        t = dt(yy,mm, dd, hh).isoformat()
        place = forecast(*PLACE, time=t)
        a = [hour.temperature for hour in place.hourly[:24]]
        data ={}
        b =1
        for x in range(len(a)):
            data[b] = a[x]
            b += 1
        return data

    
    """
    The data will be generated of a
    particular hour of a particular date.
    """
    def one_hour_temp(self, date, hour) -> float:
        lat =  self.latitude()
        longi = self.longitude()
        PLACE = self.key, lat, longi

        yy = date.year
        mm = date.month
        dd = date.day
        hh = hour
        print(self.key, lat, longi, yy, mm, dd, hh)
        print(dt(yy, mm, dd, hh))
        t = dt(yy,mm, dd, hh).isoformat()
        place = forecast(*PLACE, time=t)
        return place.hourly[hour].temperature

    """
    This will provide current tempreature 
    of the a specific place.
    """
    def current_temp(self):
        lat =  self.latitude()
        long = self.longitude()
        PLACE = self.key, lat, long
        now = dt.now()
        t = dt(now.year,now.month, now.day, now.hour).isoformat()
        place = forecast(*PLACE, time=t)
        return place['currently']['temperature']

    """
    This methode is used to
    change the location.
    """
    def change_city(self,city_name, state_name):
        self.city_name =city_name
        self.state_name =state_name
 
a = City_location("Birmingham", "Alabama","61ddd4b2d1917d2d18707c527467ad92")
temp = a.one_day_temp(dt(2019, 9, 25))
print(temp[4])


