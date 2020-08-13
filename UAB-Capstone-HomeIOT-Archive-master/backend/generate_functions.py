# Misc Imports
import os
from datetime import datetime, timedelta
from datetime import date as dt
import random
import calendar

# Import SQL Models
from models.location import Location
from models.device import Device, Electric, Water
from models.eventlog import EventLog
from models.usage import Usage
from data_generator.weather_data import *

# Import DAO Helpers
# If you don't know, DAO = Data Access Object
import dao.location as ldao
import dao.device as ddao
import dao.events as edao
import dao.usage as udao
from dao.calculate import *

# Import DB instance
from extensions.database import db

class Generator:
    __instance = None

    #Generator singleton
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Generator.__instance == None:
            print("Creating generator instance")
            Generator()
        else:
            print("Generator instance exists.. returning instance")

        return Generator.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Generator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Generator.__instance = self

    # Used to instantiate the singleton with locations/devices
    # for use when not generating data
    # since the locations/devices will have already been inserted into the database already
    def instantiateSingleton(self):
        self.kitchen =              ldao.get_location_by_name('Kitchen')
        self.kitchen_light =        ddao.get_device_by_name("kitchen_light")
        self.microwave =            ddao.get_device_by_name("microwave")
        self.refrigerator =         ddao.get_device_by_name("refrigerator")
        self.stove =                ddao.get_device_by_name("stove")
        self.oven =                 ddao.get_device_by_name("oven")
        self.dishwasher =           ddao.get_device_by_name("dishwasher")
        self.kitchen_door =         ddao.get_device_by_name("kitchen_door")
        self.kitchen_window =       ddao.get_device_by_name("kitchen_window")

        self.garage =               ldao.get_location_by_name('Garage')
        self.main_hvac =            ddao.get_device_by_name("main_hvac")
        self.garage_door =          ddao.get_device_by_name("garage_door")
        self.birmingham =           City_location("Birmingham", "Alabama", "61ddd4b2d1917d2d18707c527467ad92")
        self.water_heater =         ddao.get_device_by_name("water_heater")

        self.living_room =          ldao.get_location_by_name('Living room')
        self.livingroom_tv =        ddao.get_device_by_name("living_room_tv")
        self.livingroom_light =     ddao.get_device_by_name("living_room_light")
        self.main_door =            ddao.get_device_by_name("main_door")
        self.livingroom_window =    ddao.get_device_by_name("livingroom_window")

        """

        Adding up devices and Window to Bedroom1 

        """
        self.Bedroom1 = ldao.get_location_by_name('Bedroom1')
        self.bedroom1_light = ddao.get_device_by_name("Bedroom1_light")
        self.bedroom1_tv = ddao.get_device_by_name("bedroom1_tv")
        self.bedroom1_window = ddao.get_device_by_name("bedroom1_window")

        """

        Adding devices and windows to Bedroom2 

        """
        self.Bedroom2 = ldao.get_location_by_name('Bedroom2')
        self.bedroom2_light = ddao.get_device_by_name("Bedroom2_light")
        self.bedroom2_tv = ddao.get_device_by_name("bedroom2_tv")
        self.bedroom2_window = ddao.get_device_by_name("bedroom_window")

        """
        Adding bathroom1 and Adding devices to it

        """
        self.Bathroom1 = ldao.get_location_by_name('Bathroom1')
        self.bathroom1_exhaust_fan = ddao.get_device_by_name('bathroom1_exhaust_fan')
        self.bathroom1_light = ddao.get_device_by_name('bathroom1_light')
        self.bathroom1_bath_water_meter = ddao.get_device_by_name('bathroom1_bath_water_meter')

        """
        Adding bathroom1 and Adding devices to it

        """
        self.Bathroom2 = ldao.get_location_by_name('Bathroom2')
        self.bathroom2_exhaust_fan = ddao.get_device_by_name('bathroom2_exhaust_fan')
        self.bathroom2_light = ddao.get_device_by_name('bathroom2_light')
        self.bathroom2_shower_water_meter = ddao.get_device_by_name('bathroom2_shower_water_meter')

        """
        Adding Laundary area and Addding washer and dryer         
        """
        self.Laundary_area = ldao.get_location_by_name('Laundary_area')
        self.washer = ddao.get_device_by_name('washer')
        self.washer_water_meter = ddao.get_device_by_name('washer_water_meter')
        self.dryer = ddao.get_device_by_name('dryer')


    """
    generate locations and devices
    """
    def generate_locations_and_devices(self):
        
        self.kitchen = ldao.add_location('Kitchen')
        self.kitchen_light = ddao.add_light(self.kitchen, 0, 0, "kitchen_light", 60)
        self.microwave = ddao.add_electric_device(self.kitchen, 0, 0, "microwave", 1100)
        self.refrigerator = ddao.add_electric_device(
            self.kitchen, 920, 415, "refrigerator", 150)
        self.stove = ddao.add_electric_device(self.kitchen, 0, 0, "stove", 3000)
        self.oven = ddao.add_electric_device(self.kitchen, 935, 335, "oven", 4000)
        self.dishwasher = ddao.add_electric_device(
            self.kitchen, 0, 0, "dishwasher", 1800)
        self.kitchen_door = ddao.add_door(self.kitchen, 870, 20, "kitchen_door")
        self.kitchen_window = ddao.add_window(self.kitchen, 0, 0, "kitchen_window")

        self.garage = ldao.add_location('Garage')
        self.main_hvac = ddao.add_hvac(self.garage, 0, 0, "main_hvac", 3500)

        # Instantiate hvac devices with reasonable settings
        # Setpoint 74, high trigger 78 and low trigger 68
        # with an internal home temperature of 74
        ddao.set_hvac_params(self.main_hvac, 74, 78, 68, 74, 0)
        self.garage_door = ddao.add_door(self.garage, 568, 80, "garage_door")
        self.birmingham = City_location(
            "Birmingham", "Alabama", "61ddd4b2d1917d2d18707c527467ad92")
        self.water_heater = ddao.add_electric_device(
            self.garage, 700, 180, "water_heater", 4500)

        self.living_room = ldao.add_location('Living room')
        self.livingroom_tv = ddao.add_electric_device(
            self.living_room, 0, 0, "living_room_tv", 636)
        self.livingroom_light = ddao.add_light(
            self.living_room, 0, 0, "living_room_light", 60)
        self.main_door = ddao.add_door(self.living_room, 15, 710, "main_door")
        self.livingroom_window = ddao.add_window(
            self.living_room, 0, 0, "livingroom_window")

        """

        Adding up devices and Window to Bedroom1 

        """
        self.Bedroom1 = ldao.add_location('Bedroom1')
        self.bedroom1_light = ddao.add_light(self.Bedroom1, 0, 0, "Bedroom1_light", 60)
        self.bedroom1_tv = ddao.add_electric_device(
            self.Bedroom1, 0, 0, "bedroom1_tv", 100)
        self.bedroom1_window = ddao.add_window(self.Bedroom1, 0, 0, "bedroom1_window")

        """

        Adding devices and windows to Bedroom2 

        """
        self.Bedroom2 = ldao.add_location('Bedroom2')
        self.bedroom2_light = ddao.add_light(self.Bedroom2, 0, 0, "Bedroom2_light", 60)
        self.bedroom2_tv = ddao.add_electric_device(
            self.Bedroom2, 0, 0, "bedroom2_tv", 100)
        self.bedroom2_window = ddao.add_window(self.Bedroom2, 0, 0, "bedroom_window")

        """
        Adding bathroom1 and Adding devices to it

        """
        self.Bathroom1 = ldao.add_location('Bathroom1')
        self.bathroom1_exhaust_fan = ddao.add_electric_device(
            self.Bathroom1, 0, 0, 'bathroom1_exhaust_fan', 30)
        self.bathroom1_light = ddao.add_light(
            self.Bathroom1, 0, 0, 'bathroom1_light', 60)
        self.bathroom1_bath_water_meter = ddao.add_water_meter(
            self.Bathroom1,  0, 0, 'bathroom1_bath_water_meter')

        """
        Adding bathroom1 and Adding devices to it

        """
        self.Bathroom2 = ldao.add_location('Bathroom2')
        self.bathroom2_exhaust_fan = ddao.add_electric_device(
            self.Bathroom2, 0, 0, 'bathroom2_exhaust_fan', 30)
        self.bathroom2_light = ddao.add_light(
            self.Bathroom2, 0, 0, 'bathroom2_light', 60)
        self.bathroom2_shower_water_meter = ddao.add_water_meter(
            self.Bathroom2, 0, 0, 'bathroom2_shower_water_meter')

        """
        Adding Laundary area and Addding washer and dryer         
        """
        self.Laundary_area = ldao.add_location('Laundary_area')
        self.washer = ddao.add_electric_device(
            self.Laundary_area,  840, 140, 'washer', 500)
        self.washer_water_meter = ddao.add_water_meter(
            self.Laundary_area, 0, 0, 'washer_water_meter')
        self.dryer = ddao.add_electric_device(
            self.Laundary_area,  840, 140, 'dryer', 3000)


    """

    kitchenlight usage comuptation

    """

    def kitchen_light_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            d = random.randint(5, 7)
            start_time = given_date + timedelta(hours=d)
            on_minutes = random.randint(30, 60)
            end_time = start_time + timedelta(minutes=on_minutes)
            edao.add_event(self.kitchen_light, "ON", start_time)
            edao.add_event(self.kitchen_light, "OFF", end_time)
            n = random.randint(18, 20)
            start_time2 = given_date + timedelta(hours=n)
            on_minutes2 = random.randint(60, 180)
            end_time2 = start_time2 + timedelta(minutes=on_minutes2)
            edao.add_event(self.kitchen_light, "ON", start_time2)
            edao.add_event(self.kitchen_light, "OFF", end_time2)
            usage_minutes = on_minutes + on_minutes2
            usage = general_eq(60, timedelta(minutes=usage_minutes))
            udao.add_usage(self.kitchen_light, dates, "electric", usage/1000)
        else:
            r = random.randint(4, 5)
            usage_time = 0
            for x in range(r):
                s = random.randint(7, 20)
                start_time = given_date + timedelta(hours=s)
                on_minutes = random.randint(15, 180)
                end_time = start_time + timedelta(minutes=on_minutes)
                edao.add_event(self.kitchen_light, "ON", start_time)
                edao.add_event(self.kitchen_light, "OFF", end_time)
                usage_time += on_minutes
            usage = general_eq(60, timedelta(minutes=usage_time))
            udao.add_usage(self.kitchen_light, dates, "electric", usage/1000)


    """

    Refrigerator usage comuptation

    """


    def refrigerator_usage(self, given_date:  datetime):
        dates = given_date
        edao.add_event(self.refrigerator, "ON", dates)
        usage = general_eq(150, timedelta(hours=24))
        udao.add_usage(self.refrigerator, dates, "electric", usage / 1000)


    """

    Dishwasher usage comuptation

    """


    def dishwasher_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            r = random.randint(18, 20)
            start_time = given_date + timedelta(hours=r)
            end_time = start_time + timedelta(minutes=45)
            edao.add_event(self.dishwasher, "ON", start_time)
            edao.add_event(self.dishwasher, "OFF", end_time)
            usage = general_eq(1800, timedelta(minutes=45))
            self.water_heater_usage(start_time, 6)
            udao.add_usage(self.dishwasher, dates, "electric", usage/1000)
            udao.add_usage(self.dishwasher, dates, "water", water_usage_calculation(6))


    """

    Stove usage comuptation

    """


    def Stove_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            r = random.randint(18, 20)
            start_time = given_date + timedelta(hours=r)
            end_time = start_time + timedelta(minutes=15)
            edao.add_event(self.stove, "ON", start_time)
            edao.add_event(self.stove, "OFF", end_time)
            usage = general_eq(3500, timedelta(minutes=15))
            udao.add_usage(self.stove, dates, "electric", usage/1000)
        else:
            r = random.randint(7, 22)
            start_time = given_date + timedelta(hours=r)
            end_time = start_time + timedelta(minutes=15)
            edao.add_event(self.stove, "ON", start_time)
            edao.add_event(self.stove, "OFF", end_time)
            usage = general_eq(3500, timedelta(minutes=30))
            udao.add_usage(self.stove, dates, "electric", usage/1000)


    """

    Oven usage comuptation

    """


    def oven_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            r = random.randint(18, 21)
            start_time = given_date + timedelta(hours=r)
            end_time = start_time + timedelta(minutes=45)
            edao.add_event(self.oven, "ON", start_time)
            edao.add_event(self.oven, "OFF", end_time)
            usage = general_eq(4000, timedelta(minutes=45))
            udao.add_usage(self.oven, dates, "electric", usage/1000)
        else:
            r = random.randint(18, 21)
            start_time = given_date + timedelta(hours=r)
            end_time = start_time + timedelta(minutes=60)
            edao.add_event(self.stove, "ON", start_time)
            edao.add_event(self.stove, "OFF", end_time)
            usage = general_eq(4000, timedelta(minutes=60))
            udao.add_usage(self.oven, dates, "electric", usage/1000)


    """

    Microwave usage comuptation

    """


    def microwave_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            r = random.randint(18, 21)
            start_time = given_date + timedelta(hours=r)
            end_time = start_time + timedelta(minutes=20)
            edao.add_event(self.microwave, "ON", start_time)
            edao.add_event(self.microwave, "OFF", end_time)
            usage = general_eq(1100, timedelta(minutes=20))
            udao.add_usage(self.microwave, dates, "electric", usage/1000)
        else:
            r = random.randint(9, 21)
            start_time = given_date + timedelta(hours=r)
            end_time = start_time + timedelta(minutes=30)
            edao.add_event(self.microwave, "ON", start_time)
            edao.add_event(self.microwave, "OFF", end_time)
            usage = general_eq(1100, timedelta(minutes=30))
            udao.add_usage(self.microwave, dates, "electric", usage/1000)


    """

    Overall kicthen usage comuptation

    """


    def generate_kitchen_usage(self, start_date: datetime, end_date: datetime):
        print("Generating kitchen usage")
        days_date = end_date-start_date
        first_date = start_date
        for x in range(days_date.days):
            print(" Kitchen > ", first_date)
            self.dishwasher_usage(first_date)
            self.Stove_usage(first_date)
            self.oven_usage(first_date)
            self.microwave_usage(first_date)
            self.refrigerator_usage(first_date)
            self.kitchen_light_usage(first_date)
            first_date += timedelta(days=1)


    def water_heater_usage(self, given_date: datetime, water: float):
            start_time = given_date
            HEATER_MIN_PER_GAL = timedelta(minutes=4)
            process_time = water * HEATER_MIN_PER_GAL
            end_time = start_time + process_time
            edao.add_event(self.water_heater, "ON", start_time)
            edao.add_event(self.water_heater, "OFF", end_time)
            usage = compute_water_heater_usage(water)
            udao.add_usage(self.water_heater, given_date, "electric", usage/1000)


    """
    MAIN HVAC USAGE COMPUTATION
    """


    def main_hvac_usage(self, given_date: datetime):

        s = self.main_hvac.set_f
        h = self.main_hvac.high_f
        l = self.main_hvac.low_f
        int_temp = self.main_hvac.int_f
        temp = self.birmingham.one_day_temp(given_date)

        #print("Starting hvac usage using hvac values from database: ", s, h, l)

        times = 0
        usage = 0
        timeswas = 0

        for x in range(24):
            out_temp = temp[x+1]
            for m in range(60):
                dates = given_date + timedelta(hours=x) + timedelta(minutes=m)
                betweenfirst = dates - timedelta(minutes=1)

                betweenlast = dates
                # door_count = EventLog.query.filter(EventLog.date.between(dates - timedelta(minutes = 1), dates), EventLog.state == 'OPENDOOR').count()
                # window_count = EventLog.query.filter(EventLog.date.between(dates - timedelta(minutes = 1), dates ), EventLog.state == 'OPENWINDOW').count()
                door_count = db.engine.execute(
                    f"SELECT COUNT(*) FROM EventLog WHERE state = 'OPENDOOR' AND date BETWEEN '{betweenfirst.strftime('%Y-%m-%d %H:%M:%S')}' AND '{betweenlast.strftime('%Y-%m-%d %H:%M:%S')}'").first()[0]
                window_count = db.engine.execute(
                    f"SELECT COUNT(*) FROM EventLog WHERE state = 'OPENWINDOW' AND date BETWEEN '{betweenfirst.strftime('%Y-%m-%d %H:%M:%S')}' AND '{betweenlast.strftime('%Y-%m-%d %H:%M:%S')}'").first()[0]
                int_temp = get_new_interior_temperature(int_temp, out_temp, door_count, window_count)

                if times > 0:
                    usage += general_eq(3500, timedelta(minutes=1))
                    # edao.add_hvac_event(self.main_hvac, "ON", int_temp, dates)
                    # edao.add_hvac_event(self.main_hvac, "OFF", int_temp,
                    #                     dates+timedelta(minutes=1))
                    int_temp = get_new_HVAC_temperature(int_temp, s)
                    
                    times -= 1
                    if times <= 0 or m >= 59:
                        #print("HVAC turned off, int temp: ", int_temp, "Usage: ", usage/1000, " Times was: ", timeswas)

                        udao.add_usage(self.main_hvac, dates, "electric", usage/1000)
                        edao.add_out_temperature_log(self.main_hvac, out_temp, dates)
                        edao.add_int_temperature_log(self.main_hvac, int_temp, dates)
                        ddao.set_hvac_params(self.main_hvac, s, h, l, int_temp, out_temp)

                        usage = 0
                else:
                    if int_temp >= h or int_temp <= l:
                        times += round(abs(int_temp - s))
                        timeswas = times
                        #print("HVAC Triggered Int temp: ", int_temp, "Setpoint: ", s, " External Temp: ", out_temp)


    """

    Livingroom TV usage computation

    """
    def livingroom_tv_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            r = random.randint(16, 18)
            start_time = given_date + timedelta(hours = r)
            end_time = start_time + timedelta(hours = 4)
            edao.add_event(self.livingroom_tv, "ON", start_time)
            edao.add_event(self.livingroom_tv, "OFF", end_time )
            usage = general_eq(636,timedelta(minutes = 240))
            udao.add_usage(self.livingroom_tv, dates, "electric", usage/1000)
        else: 
            r = random.randint(9, 16)
            start_time = given_date + timedelta(hours = r)
            end_time = start_time + timedelta(hours = 8)
            edao.add_event(self.livingroom_tv, "ON", start_time)
            edao.add_event(self.livingroom_tv, "OFF", end_time)
            usage =  general_eq(636,timedelta(minutes = 480))
            udao.add_usage(self.livingroom_tv, dates, "electric", usage /1000)



    """

    Usag of Doors computation

    """
    def door_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            for d in range(16):
                if d <= 3:
                    r = random.randint(28, 30)
                    start_time = given_date + timedelta(hours = 7) + timedelta(minutes = r)
                    end_time = start_time + timedelta(seconds = 30)
                    door_selection = random.randint(1,2)
                    if door_selection ==1:
                        edao.add_event(self.main_door, "OPENDOOR", start_time)
                        edao.add_event(self.main_door, "CLOSEDOOR", end_time)
                    elif door_selection ==2:
                        edao.add_event(self.garage_door, "OPENDOOR", start_time)
                        edao.add_event(self.garage_door, "CLOSEDOOR", end_time)
                        
                elif d == 4 and d == 5:
                    r = random.randint(0,5)
                    start_time = given_date + timedelta(hours = 16) + timedelta(minutes = r)
                    end_time = start_time + timedelta(seconds = 30)
                    door_selection = random.randint(1,2)
                
                    if door_selection ==1:
                        edao.add_event(self.main_door, "OPENDOOR", start_time)
                        edao.add_event(self.main_door, "CLOSEDOOR", end_time)
                    elif door_selection ==2:
                        edao.add_event(self.garage_door, "OPENDOOR", start_time)
                        edao.add_event(self.garage_door, "CLOSEDOOR", end_time)
                    
                elif d == 6 and d == 7:
                    r = random.randint(30, 35)
                    start_time = given_date + timedelta(hours = 17) + timedelta(minutes = r)
                    end_time = start_time + timedelta(seconds = 30)
                    door_selection = random.randint(1,2)
                    if door_selection ==1:
                        edao.add_event(self.main_door, "OPENDOOR", start_time)
                        edao.add_event(self.main_door, "CLOSEDOOR", end_time)
                    elif door_selection ==2:
                        edao.add_event(self.garage_door, "OPENDOOR", start_time)
                        edao.add_event(self.garage_door, "CLOSEDOOR", end_time)
                else:
                    hh = random.randint(6, 22)
                    mm = random.randint(0,59)
                    door_selection= random.randint(1,3)
                    start_time = given_date + timedelta(hours = hh ) + timedelta(minutes = mm)
                    end_time = start_time + timedelta(seconds = 30)
                    if door_selection == 1:
                        edao.add_event(self.main_door, "OPENDOOR", start_time)
                        edao.add_event(self.main_door, "CLOSEDOOR", end_time)
                        
                    elif door_selection == 2:
                        edao.add_event(self.garage_door, "OPENDOOR", start_time)
                        edao.add_event(self.garage_door, "CLOSEDOOR", end_time)   
                    elif door_selection == 3:
                        edao.add_event(self.kitchen_door, "OPENDOOR", start_time)
                        edao.add_event(self.kitchen_door, "CLOSEDOOR", end_time)
        else:
            for x in range(32):
                hh = random.randint(0, 22)
                mm = random.randint(0,59)
                door_selection= random.randint(1,3)
                start_time = given_date + timedelta(hours = hh ) + timedelta(minutes = mm)
                end_time = start_time + timedelta(seconds = 30)
                
                if door_selection == 1:
                    edao.add_event(self.main_door, "OPENDOOR", start_time)
                    edao.add_event(self.main_door, "CLOSEDOOR", end_time)
                        
                elif door_selection == 2:
                    edao.add_event(self.garage_door, "OPENDOOR", start_time)
                    edao.add_event(self.garage_door, "CLOSEDOOR", end_time)   
                elif door_selection == 3:
                    edao.add_event(self.kitchen_door, "OPENDOOR", start_time)
                    edao.add_event(self.kitchen_door, "CLOSEDOOR", end_time)
    """
    Window Usage computation
    """
    def window_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            for d in range(random.randint(0, 10)):
                if d <= 1:
                    r = random.randint(28, 30)
                    start_time = given_date + timedelta(hours = 7) + timedelta(minutes = r)
                    open_time = random.randint(4, 20)
                    end_time = start_time + timedelta(minutes = open_time)
                    window_selection = random.randint(1,3)
                    if window_selection ==1:
                        edao.add_event(self.livingroom_window, "OPENWINDOW", start_time)
                        edao.add_event(self.livingroom_window, "CLOSEWINDOW", end_time)
                    elif window_selection ==2:
                        edao.add_event(self.kitchen_window, "OPENWINDOW", start_time)
                        edao.add_event(self.kitchen_window, "CLOSEWINDOW", end_time)
                    elif window_selection == 3:
                        edao.add_event(self.bedroom1_window, "OPENWINDOW", start_time)
                        edao.add_event(self.bedroom1_window, "CLOSEWINDOW", end_time)
                    elif window_selection == 4:
                        edao.add_event(self.bedroom2_window, "OPENWINDOW", start_time)
                        edao.add_event(self.bedroom2_window, "CLOSEWINDOW", end_time)

                else:
                    hh = random.randint(6, 22)
                    mm = random.randint(0,59)
                    door_selection= random.randint(1,2)
                    start_time = given_date + timedelta(hours = hh ) + timedelta(minutes = mm)
                    open_time = random.randint(4, 30)
                    end_time = start_time + timedelta(minutes = open_time)
                    window_selection = random.randint(1,4)
                    if window_selection ==1:
                        edao.add_event(self.livingroom_window, "OPENWINDOW", start_time)
                        edao.add_event(self.livingroom_window, "CLOSEWINDOW", end_time)
                    elif window_selection ==2:
                        edao.add_event(self.kitchen_window, "OPENWINDOW", start_time)
                        edao.add_event(self.kitchen_window, "CLOSEWINDOW", end_time)
                    elif window_selection == 3:
                        edao.add_event(self.bedroom1_window, "OPENWINDOW", start_time)
                        edao.add_event(self.bedroom1_window, "CLOSEWINDOW", end_time)
                    elif window_selection == 4:
                        edao.add_event(self.bedroom2_window, "OPENWINDOW", start_time)
                        edao.add_event(self.bedroom2_window, "CLOSEWINDOW", end_time)
        else:
            for x in range(32):
                hh = random.randint(0, 22)
                mm = random.randint(0,59)
                door_selection= random.randint(1,2)
                start_time = given_date + timedelta(hours = hh ) + timedelta(minutes = mm)
                end_time = start_time + timedelta(seconds = 30)
                window_selection = random.randint(1,4)
                if window_selection ==1:
                    edao.add_event(self.livingroom_window, "OPENWINDOW", start_time)
                    edao.add_event(self.livingroom_window, "CLOSEWINDOW", end_time)
                elif window_selection ==2:
                    edao.add_event(self.kitchen_window, "OPENWINDOW", start_time)
                    edao.add_event(self.kitchen_window, "CLOSEWINDOW", end_time)
                elif window_selection == 3:
                    edao.add_event(self.bedroom1_window, "OPENWINDOW", start_time)
                    edao.add_event(self.bedroom1_window, "CLOSEWINDOW", end_time)
                elif window_selection == 4:
                    edao.add_event(self.bedroom2_window, "OPENWINDOW", start_time)
                    edao.add_event(self.bedroom2_window, "CLOSEWINDOW", end_time)

    """

    Living Room light usage Computation 

    """
    def livingroom_light_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            d = random.randint(5, 6)
            start_time = given_date + timedelta(hours = d)
            on_minutes = random.randint(30, 60)
            end_time = start_time + timedelta(minutes = on_minutes) 
            edao.add_event(self.livingroom_light, "ON", start_time)
            edao.add_event(self.livingroom_light, "OFF", end_time)
            n = random.randint(18, 20)
            start_time2 = given_date + timedelta(hours = n)
            on_minutes2 = random.randint(60, 180)
            end_time2 = start_time2 + timedelta(minutes = on_minutes2) 
            edao.add_event(self.livingroom_light, "ON", start_time2)
            edao.add_event(self.livingroom_light, "OFF", end_time2) 
            usage_minutes = on_minutes + on_minutes2 
            usage = general_eq(60, timedelta(minutes =usage_minutes))
            udao.add_usage(self.livingroom_light, dates, "electric", usage/1000)
        else:
            r = random.randint(4, 5)
            usage_time = 0
            for x in range(r):
                s = random.randint(7, 20)
                start_time = given_date + timedelta(hours = s)
                on_minutes = random.randint(15 , 180)
                end_time = start_time + timedelta(minutes =on_minutes)
                edao.add_event(self.livingroom_light, "ON", start_time)
                edao.add_event(self.livingroom_light, "OFF", end_time)
                usage_time += on_minutes
            usage = general_eq(60, timedelta(minutes =usage_time))
            udao.add_usage(self.livingroom_light, dates, "electric", usage/1000)


    """

    Bedroom1 light usage Computation

    """

    def bedroom1_light_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            d = random.randint(5, 7)
            start_time = given_date + timedelta(hours = d)
            on_minutes = random.randint(30, 60)
            end_time = start_time + timedelta(minutes = on_minutes) 
            edao.add_event(self.bedroom1_light, "ON", start_time)
            edao.add_event(self.bedroom1_light, "OFF", end_time)
            n = random.randint(18, 22)
            start_time2 = given_date + timedelta(hours = n)
            on_minutes2 = random.randint(60, 180)
            end_time2 = start_time2 + timedelta(minutes = on_minutes2) 
            edao.add_event(self.bedroom1_light, "ON", start_time2)
            edao.add_event(self.bedroom1_light, "OFF", end_time2) 
            usage_minutes = on_minutes + on_minutes2 
            usage = general_eq(60, timedelta(minutes =usage_minutes))
            udao.add_usage(self.bedroom1_light, dates, "electric", usage/1000)
        else:
            r = random.randint(4, 5)
            usage_time = 0
            for x in range(r):
                s = random.randint(7, 22)
                start_time = given_date + timedelta(hours = s)
                on_minutes = random.randint(15 , 180)
                end_time = start_time + timedelta(minutes =on_minutes)
                edao.add_event(self.bedroom1_light, "ON", start_time)
                edao.add_event(self.bedroom1_light, "OFF", end_time)
                usage_time += on_minutes
            usage = general_eq(60, timedelta(minutes =usage_time))
            udao.add_usage(self.bedroom1_light, dates, "electric", usage/1000)


    """

    Bedroom1 Tv usage Computation

    """
    def bedroom1_tv_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            r = random.randint(20, 22)
            start_time = given_date + timedelta(hours = r)
            end_time = start_time + timedelta(hours = 2)
            edao.add_event(self.bedroom1_tv, "ON", start_time)
            edao.add_event(self.bedroom1_tv, "OFF", end_time )
            usage = general_eq(100,timedelta(minutes = 120))
            udao.add_usage(self.bedroom1_tv, dates, "electric", usage/1000)
        else: 
            r = random.randint(9, 22)
            start_time = given_date + timedelta(hours = r)
            end_time = start_time + timedelta(hours = 4)
            edao.add_event(self.bedroom1_tv, "ON", start_time)
            edao.add_event(self.bedroom1_tv, "OFF", end_time)
            usage = general_eq(100,timedelta(minutes = 240))
            udao.add_usage(self.bedroom1_tv, dates, "electric", usage/1000)



    """

    Bedroom2 light usage Computation

    """
    def bedroom2_light_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            d = random.randint(5, 6)
            start_time = given_date + timedelta(hours = d)
            on_minutes = random.randint(30, 60)
            end_time = start_time + timedelta(minutes = on_minutes) 
            edao.add_event(self.bedroom1_light, "ON", start_time)
            edao.add_event(self.bedroom1_light, "OFF", end_time)
            n = random.randint(18, 20)
            start_time2 = given_date + timedelta(hours = n)
            on_minutes2 = random.randint(60, 180)
            end_time2 = start_time2 + timedelta(minutes = on_minutes2) 
            edao.add_event(self.bedroom1_light, "ON", start_time2)
            edao.add_event(self.bedroom1_light, "OFF", end_time2) 
            usage_minutes = on_minutes + on_minutes2 
            usage = general_eq(60, timedelta(minutes =usage_minutes))
            udao.add_usage(self.bedroom1_light, dates, "electric", usage/1000)
        else:
            r = random.randint(4, 5)
            usage_time = 0
            for x in range(r):
                s = random.randint(7, 20)
                start_time = given_date + timedelta(hours = s)
                on_minutes = random.randint(15 , 180)
                end_time = start_time + timedelta(minutes = on_minutes)
                edao.add_event(self.bedroom1_light, "ON", start_time)
                edao.add_event(self.bedroom1_light, "OFF", end_time)
                usage_time += on_minutes
            usage = general_eq(60, timedelta(minutes =usage_time))
            udao.add_usage(self.bedroom1_light, dates, "electric", usage/1000)

    """

    Bedroom2 Tv usage Computation

    """
    def bedroom2_tv_usage(self, given_date: datetime):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            r = random.randint(16, 20)
            start_time = given_date + timedelta(hours = r)
            end_time = start_time + timedelta(hours = 2)
            edao.add_event(self.bedroom2_tv, "ON", start_time)
            edao.add_event(self.bedroom2_tv, "OFF", end_time )
            usage = general_eq(100,timedelta(minutes = 120))
            udao.add_usage(self.bedroom2_tv, dates, "electric", usage/1000)
        else: 
            r = random.randint(9, 20)
            start_time = given_date + timedelta(hours = r)
            end_time = start_time + timedelta(hours = 4)
            edao.add_event(self.bedroom2_tv, "ON", start_time)
            edao.add_event(self.bedroom2_tv, "OFF", end_time)
            usage = general_eq(100,timedelta(minutes = 240))
            udao.add_usage(self.bedroom2_tv, dates, "electric", usage/1000)


    def bathroom1_light_usage(self, given_date: datetime, usage_start_time: int):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            start_time = given_date + timedelta(hours = usage_start_time)
            on_minutes = random.randint(45, 60)
            end_time = start_time + timedelta(minutes = on_minutes) 
            edao.add_event(self.bathroom1_light, "ON", start_time)
            edao.add_event(self.bathroom1_light, "OFF", end_time)
            usage = general_eq(60, timedelta(minutes = on_minutes))
            udao.add_usage(self.bathroom1_light, dates, "electric", usage/1000)
        else:
            r = random.randint(1, 3)
            usage_time = 0
            for x in range(r):
                s = random.randint(7, 20)
                start_time = given_date + timedelta(hours = s)
                on_minutes = random.randint(20 , 60)
                end_time = start_time + timedelta(minutes = on_minutes)
                edao.add_event(self.bathroom1_light, "ON", start_time)
                edao.add_event(self.bathroom1_light, "OFF", end_time)
                usage_time += on_minutes
            usage = general_eq(60, timedelta(minutes =on_minutes))
            udao.add_usage(self.bathroom1_light, dates, "electric", usage/1000)

    def bathroom1_exhaust_fan_usage(self, given_date: datetime, starting_time:int, on_minutes:int):
        dates = given_date
        start_time = starting_time
        end_time = start_time + timedelta(minutes = on_minutes)
        edao.add_event(self.bathroom1_exhaust_fan, "ON", start_time)
        edao.add_event(self.bathroom1_exhaust_fan, "OFF", end_time)
        usage = general_eq(60, timedelta(minutes = on_minutes))
        udao.add_usage(self.bathroom1_exhaust_fan, dates, "electric", usage/1000)

    def bathroom1_bath_water_meter_usage(self, given_date: datetime, usage_start_time: int, times: int):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        heater_water = 30 * 0.65
        if times == 2:
            start_time = given_date + timedelta(hours = usage_start_time)
            on_minutes = random.randint(20, 25)
            end_time = start_time + timedelta(minutes = on_minutes)
            self.bathroom1_exhaust_fan_usage(given_date, start_time, on_minutes)
            self.water_heater_usage(start_time, heater_water) 
            edao.add_event(self.bathroom1_bath_water_meter, "ON", start_time)
            edao.add_event(self.bathroom1_bath_water_meter, "OFF", end_time)
            usage = water_usage_calculation(30)
            udao.add_usage(self.bathroom1_bath_water_meter, dates, "water", usage)
            # Time2
            start_time2 = end_time +timedelta(minutes = 5)
            on_minutes2 = random.randint(20,25)
            end_time2 = start_time2 + timedelta(minutes = on_minutes2)
            edao.add_event(self.bathroom1_bath_water_meter, "ON", start_time2)
            edao.add_event(self.bathroom1_bath_water_meter, "OFF", end_time2)
            self.bathroom1_exhaust_fan_usage(given_date, start_time2, on_minutes2) 
            self.water_heater_usage(start_time2, heater_water)
            usage1 = water_usage_calculation(30)
            udao.add_usage(self.bathroom1_bath_water_meter, dates, "water", usage1)
        else:
            start_time = given_date + timedelta(hours = usage_start_time)
            on_minutes = random.randint(20, 25)
            end_time = start_time + timedelta(minutes = on_minutes)
            self.bathroom1_exhaust_fan_usage(given_date, start_time, on_minutes) 
            self.water_heater_usage(start_time, heater_water)
            edao.add_event(self.bathroom1_bath_water_meter, "ON", start_time)
            edao.add_event(self.bathroom1_bath_water_meter, "OFF", end_time)
            usage = water_usage_calculation(30)
            udao.add_usage(self.bathroom1_bath_water_meter, dates, "water", usage)
            # Time 2
            start_time2 = end_time +timedelta(minutes = 5)
            on_minutes2 = random.randint(20,25)
            end_time2 = start_time2 + timedelta(minutes = on_minutes2)
            edao.add_event(self.bathroom1_bath_water_meter, "ON", start_time2)
            edao.add_event(self.bathroom1_bath_water_meter, "OFF", end_time2)
            self.bathroom1_exhaust_fan_usage(given_date, start_time2, on_minutes2) 
            self.water_heater_usage(start_time2, heater_water)
            usage2 = water_usage_calculation(30)
            udao.add_usage(self.bathroom1_bath_water_meter, dates, "water", usage2)
            # Time 3
            start_time3 = end_time2 +timedelta(hours = 3)
            on_minutes3 = random.randint(20,25)
            end_time3 = start_time3 + timedelta(minutes = on_minutes3)
            edao.add_event(self.bathroom1_bath_water_meter, "ON", start_time3)
            edao.add_event(self.bathroom1_bath_water_meter, "OFF", end_time3)
            self.bathroom1_exhaust_fan_usage(given_date, start_time3, on_minutes3) 
            self.water_heater_usage(start_time3, heater_water)
            usage3 = water_usage_calculation(30)
            udao.add_usage(self.bathroom1_bath_water_meter, dates, "water", usage3)


    def bathroom2_light_usage(self, given_date: datetime, usage_start_time: int):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
            start_time = given_date + timedelta(hours = usage_start_time)
            on_minutes = random.randint(45, 60)
            end_time = start_time + timedelta(minutes = on_minutes) 
            edao.add_event(self.bathroom2_light, "ON", start_time)
            edao.add_event(self.bathroom2_light, "OFF", end_time)
            usage = general_eq(60, timedelta(minutes = on_minutes))
            udao.add_usage(self.bathroom2_light, dates, "electric", usage/1000)
        else:
            r = random.randint(1, 3)
            usage_time = 0
            for x in range(r):
                s = random.randint(7, 20)
                start_time = given_date + timedelta(hours = s)
                on_minutes = random.randint(20 , 60)
                end_time = start_time + timedelta(minutes = on_minutes)
                edao.add_event(self.bathroom2_light, "ON", start_time)
                edao.add_event(self.bathroom2_light, "OFF", end_time)
                usage_time += on_minutes
            usage = general_eq(60, timedelta(minutes =on_minutes))
            udao.add_usage(self.bathroom2_light, dates, "electric", usage/1000)

    def bathroom2_exhaust_fan_usage(self, given_date: datetime, starting_time:int, on_minutes:int):
        dates = given_date
        start_time = starting_time
        end_time = start_time + timedelta(minutes = on_minutes)
        edao.add_event(self.bathroom2_exhaust_fan, "ON", start_time)
        edao.add_event(self.bathroom2_exhaust_fan, "OFF", end_time)
        usage = general_eq(60, timedelta(minutes = on_minutes))
        udao.add_usage(self.bathroom2_exhaust_fan, dates, "electric", usage/1000)

    def bathroom2_shower_water_meter_usage(self, given_date: datetime, usage_start_time: int, times: int):
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        heater_water = 25 * 0.65
        if times == 2:
            start_time = given_date + timedelta(hours = usage_start_time)
            on_minutes = random.randint(20, 25)
            end_time = start_time + timedelta(minutes = on_minutes)
            self.bathroom2_exhaust_fan_usage(given_date, start_time, on_minutes) 
            self.water_heater_usage(start_time, heater_water)
            edao.add_event(self.bathroom2_shower_water_meter, "ON", start_time)
            edao.add_event(self.bathroom2_shower_water_meter, "OFF", end_time)
            usage = water_usage_calculation(25)
            udao.add_usage(self.bathroom2_shower_water_meter, dates, "water", usage)
            # Time2
            start_time2 = end_time +timedelta(minutes = 5)
            on_minutes2 = random.randint(20,25)
            end_time2 = start_time2 + timedelta(minutes = on_minutes2)
            edao.add_event(self.bathroom2_shower_water_meter, "ON", start_time2)
            edao.add_event(self.bathroom2_shower_water_meter, "OFF", end_time2)
            self.bathroom2_exhaust_fan_usage(given_date, start_time2, on_minutes2)
            self.water_heater_usage(start_time2, heater_water) 
            usage1 = water_usage_calculation(25)
            udao.add_usage(self.bathroom2_shower_water_meter, dates, "water", usage1)
        else:
            start_time = given_date + timedelta(hours = usage_start_time)
            on_minutes = random.randint(20, 25)
            end_time = start_time + timedelta(minutes = on_minutes)
            self.bathroom2_exhaust_fan_usage(given_date, start_time, on_minutes)
            self.water_heater_usage(start_time, heater_water) 
            edao.add_event(self.bathroom2_shower_water_meter, "ON", start_time)
            edao.add_event(self.bathroom2_shower_water_meter, "OFF", end_time)
            usage = water_usage_calculation(25)
            udao.add_usage(self.bathroom2_shower_water_meter, dates, "water", usage)
            # Time 2
            start_time2 = end_time +timedelta(minutes = 5)
            on_minutes2 = random.randint(20,25)
            end_time2 = start_time2 + timedelta(minutes = on_minutes2)
            edao.add_event(self.bathroom2_shower_water_meter, "ON", start_time2)
            edao.add_event(self.bathroom2_shower_water_meter, "OFF", end_time2)
            self.bathroom2_exhaust_fan_usage(given_date, start_time2, on_minutes2)
            self.water_heater_usage(start_time2, heater_water) 
            usage2 = water_usage_calculation(25)
            udao.add_usage(self.bathroom2_shower_water_meter, dates, "water", usage2)
            # Time 3
            start_time3 = end_time2 +timedelta(hours = 3)
            on_minutes3 = random.randint(20,25)
            end_time3 = start_time3 + timedelta(minutes = on_minutes3)
            edao.add_event(self.bathroom2_shower_water_meter, "ON", start_time3)
            edao.add_event(self.bathroom2_shower_water_meter, "OFF", end_time3)
            self.bathroom2_exhaust_fan_usage(given_date, start_time3, on_minutes3) 
            self.water_heater_usage(start_time3, heater_water)
            usage3 = water_usage_calculation(25)
            udao.add_usage(self.bathroom2_shower_water_meter, dates, "water", usage3)


    def washer_usage(self, given_date: datetime):
        print("Generating washer usage")
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        if days == "Saturday" or days == "Sunday":
            r = random.randint(10, 19)
            start_time = given_date + timedelta(hours = r)
            end_time = start_time + timedelta(minutes = 30)
            edao.add_event(self.washer, "ON", start_time)
            edao.add_event(self.washer, "OFF", end_time)
            self.dryer_usage(end_time+ timedelta(minutes =10) )   ##calling dryer methode to start 
            usage = general_eq(500 ,timedelta(minutes = 30))
            self.water_heater_usage(start_time, 20 * 0.85)       ##calling heater methode to start 
            udao.add_usage(self.washer, dates, "electric", usage/1000)
            udao.add_usage(self.washer_water_meter, dates, "water", water_usage_calculation(20))
            start_time2 = given_date + end_time + timedelta(minutes )
            end_time2 = start_time2 + timedelta(minutes = 30)
            edao.add_event(self.washer, "ON", start_time2)
            edao.add_event(self.washer, "OFF", end_time2)
            self.dryer_usage(end_time2+ timedelta(minutes =10)) ##calling dryer methode to start
            self.water_heater_usage(start_time2, 20 * 0.85)     ##calling heater methode to start
            usage2 = general_eq(500 ,timedelta(minutes = 30))
            udao.add_usage(self.washer, dates, "electric", usage2/1000)
            udao.add_usage(self.washer_water_meter, dates, "water", water_usage_calculation(20))

    def dryer_usage(self, given_date: datetime):
        print("Generating dryer usage")
        dates = given_date
        days = calendar.day_name[dates.weekday()]
        start_time = given_date
        end_time = start_time + timedelta(minutes = 30)
        edao.add_event(self.dryer, "ON", start_time)
        edao.add_event(self.dryer, "OFF", end_time)
        usage = general_eq(3000 ,timedelta(minutes = 30))
        udao.add_usage(self.dryer, dates, "electric", usage)


        

    """

    Giving start date and end date of which
    user wants to compute data for Bedroom1.

    """
    def Bedroom1_usage(self, start_date: datetime, end_date: datetime):      
        print("Generating bedroom1 usage")          
        days_date = end_date-start_date
        first_date = start_date
        for x in range(days_date.days):
            if(first_date == dt.today()):
                break
            self.bedroom1_tv_usage(first_date)
            self.bedroom1_light_usage(first_date)
            first_date += timedelta(days=1)


    """

    Giving start date and end date of which
    user wants to compute data for Bedroom2.

    """
    def Bedroom2_usage(self, start_date: datetime, end_date: datetime):       
        print("Generating bedroom2 usage")         
        days_date = end_date-start_date
        first_date = start_date
        for x in range(days_date.days + 1):
            if(first_date == dt.today()):
                break
            self.bedroom2_tv_usage(first_date)
            self.bedroom2_light_usage(first_date)
            first_date += timedelta(days=1)



    """

    Giving start date and end date of which
    user wants to compute data for Livingroom.

    """
    def living_room_usage(self, start_date: datetime, end_date: datetime):     
        print("Generating living room usage")           
        days_date = end_date-start_date
        first_date = start_date
        for x in range(days_date.days + 1):
            if(first_date == dt.today()):
                break
            self.livingroom_tv_usage(first_date)
            self.livingroom_light_usage(first_date)
            first_date += timedelta(days=1)

    """

    Giving start date and end date of which
    user wants to compute data for doors.

    """
    def door_action(self, start_date: datetime, end_date: datetime):
        print("Generating door actions")
        days_date = end_date-start_date
        first_date = start_date
        for x in range(days_date.days + 1):
            if(first_date == dt.today()):
                break
            self.door_usage(first_date)
            first_date += timedelta(days=1)

    """

    Giving start date and end date of which
    user wants to compute data for windows.

    """
    def window_action(self, start_date: datetime, end_date: datetime ):
        print("Generating window actions" )
        days_date = end_date-start_date
        first_date = start_date
        for x in range(days_date.days + 1):
            if(first_date == dt.today()):
                break
            self.window_usage(first_date)
            first_date += timedelta(days=1)

    """

    Giving start date and end date of which
    user wants to compute data for Garage.

    """
    def garage_usage(self, start_date: datetime, end_date: datetime ):
        print("Generating garage usage")
        days_date = end_date - start_date
        first_date = start_date
        for x in range(days_date.days + 1):
            print(" Garage > ",first_date)
            if(first_date == dt.today()):
                break
            self.main_hvac_usage(first_date)
            first_date += timedelta(days=1) 



    """

    Giving start date and end date of which
    user wants to compute data for Bathroom1.

    """
    def Bathroom1_usage(self, start_date: datetime, end_date: datetime ):
        print("Generating bathroom1_usage")
        days_date = end_date - start_date
        first_date = start_date

        for x in range(days_date.days + 1):
            days = calendar.day_name[first_date.weekday()]
            if(first_date == dt.today()):
                break
            
            if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
                usage_time = random.randint(5, 6)
                self.bathroom1_light_usage(first_date, usage_time)
                self.bathroom1_bath_water_meter_usage(first_date, usage_time, 2)
            else:
                usage_time = random.randint(7, 19)
                self.bathroom1_bath_water_meter_usage(first_date, usage_time, 3)
                self.bathroom1_light_usage(first_date, usage_time)
            first_date += timedelta(days=1) 


    def Bathroom2_usage(self, start_date: datetime, end_date: datetime ):
        print("Generating bathroom2 usage")
        days_date = end_date - start_date
        first_date = start_date

        for x in range(days_date.days + 1):                
            days = calendar.day_name[first_date.weekday()]
            if(first_date == dt.today()):
                break
            
            if days == "Monday" or days == "Tuesday" or days == "Wednesday" or days == "Thursday" or days == "Friday":
                usage_time = random.randint(5, 6)
                self.bathroom2_light_usage(first_date, usage_time)
                self.bathroom2_shower_water_meter_usage(first_date, usage_time, 2)
            else:
                usage_time = random.randint(7, 19)
                self.bathroom2_shower_water_meter_usage(first_date, usage_time, 3)
                self.bathroom2_light_usage(first_date, usage_time)
            first_date += timedelta(days=1) 


    """

    Giving start date and end date of which
    user wants to compute data for entire home.

    """
    def home_usage(self, start: datetime, end: datetime):
        self.generate_kitchen_usage(start, end) ## calls generate_kitchen_usage
        self.Bedroom1_usage(start, end)  ## calls Bedroom1_usage
        self.door_action(start,end)  ## calls door_usage
        self.window_action(start, end)  ## calls window_usage
        self.Bedroom2_usage(start, end)  ## calls Bedroom2_usage
        self.living_room_usage(start, end)  ## calls Livingroom_usage
        self.garage_usage(start, end)  ## calls garage_usage
        self.Bathroom1_usage(start, end)
        self.Bathroom2_usage(start, end)

    def get_next_date_to_generate(self):
        try:
            lastusageentry = udao.get_last_usage_entry()
            lastusagedate = lastusageentry.date
            nextusagedate = lastusagedate + timedelta(days=1)

            return datetime(nextusagedate.year, nextusagedate.month, nextusagedate.day)
        except:
            return datetime.now()

    def on_demand_electric_usage(self, device: Electric, start_time: datetime, end_time: datetime):
        edao.add_event(device, "ON", start_time)
        edao.add_event(device, "OFF", end_time)

        # Get timedelta from start-end
        t_delta = end_time - start_time
        # Convert seconds to minutes to use in general_eq
        on_minutes = t_delta.seconds / 60

        usage = general_eq(device.wattage, timedelta(minutes=on_minutes))
        usage_kwh = usage/1000
        print("Adding on demand usage for device: On time: ", on_minutes, " Total KWH: ", usage_kwh)
        udao.add_usage(device, end_time, "electric", usage_kwh)

        return {
            'usage': usage_kwh
        }

    def generate_next_day_auto(self):
        nextdate = self.get_next_date_to_generate()
        nextdate = datetime(nextdate.year, nextdate.month, nextdate.day, 0, 0)
        enddate = datetime(nextdate.year, nextdate.month, nextdate.day, 23, 59)

        print(nextdate)
        print(enddate)

        print("Generating data for next day...")
        self.home_usage(nextdate, enddate)
        print("Done generating data for next day")