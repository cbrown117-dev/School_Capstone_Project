from typing import List

import datetime
import calendar

from models.usage import Usage
from models.device import Device
from extensions.database import commit
from extensions.database import db

from sqlalchemy import func

import numpy as np
import scipy
from sklearn.linear_model import LinearRegression

from dao.calculate import kwh_to_dollars, gallons_to_dollars

from datetime import timedelta

def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


def add_usage(device: Device, date, type: str, data: float) -> Usage:
    """

    :param device: deviceId
    :param date: DATETIME
    :param type: water/electric
    :param data: gallons/kWh
    :return:
    """
    assert data > 0

    usageData = Usage(device, date, type, data)
    
    commit(usageData)
    return usageData


def get_usages(startdate: str, enddate: str, type: str, ascending: bool) -> List[Usage]:
    """
    :param startdate: Start date in ISO format
    :param enddate: End date in ISO format
    :param type: water/electric
    :param ascending: sorting type
    :return:
    """
    if startdate and enddate:
        return Usage.query \
            .filter(Usage.date.between(startdate, enddate)) \
            .filter(Usage.type == type) \
            .order_by(Usage.date.asc()) \
            .all()
    else:
        return Usage.query \
            .filter(Usage.type == type) \
            .order_by(Usage.date.asc()) \
            .all()

def get_device_total_usage(deviceid: int, startdate: str, enddate: str) -> int:
    if startdate and enddate:
        return Usage.query.with_entities(func.sum(Usage.data) \
            .label("usage_total")) \
            .filter(Usage.date.between(startdate, enddate)) \
            .filter(Usage.deviceId == deviceid) \
            .first()[0]
    else:
        return Usage.query.with_entities(func.sum(Usage.data) \
            .label("usage_total")) \
            .filter(Usage.deviceId == deviceid) \
            .first()[0]

def get_last_usage_entry() -> Usage:
    return Usage.query.order_by(Usage.date.desc()).first()

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def get_statistics(start):
    # Get start date as datetime
    startdt = datetime.datetime.strptime(start, '%Y-%m-%d')
    enddt = last_day_of_month(startdt) # Calculate last day of the current month

    # Convert back to ISO format for sql purposes
    start = startdt.strftime('%Y-%m-%d')
    end = enddt.strftime('%Y-%m-%d')

    daily_electric = db.engine.execute(f"SELECT date_trunc('day', date) as daterange, sum(data) FROM usage WHERE type = 'electric' AND date BETWEEN '{start}' AND '{end}' GROUP BY 1;")
    daily_water = db.engine.execute(f"SELECT date_trunc('day', date) as daterange, sum(data) FROM usage WHERE type = 'water' AND date BETWEEN '{start}' AND '{end}' GROUP BY 1;")

    sum_elec = 0
    sum_water = 0

    for date, data in daily_electric:
        sum_elec += data
    
    for date, data in daily_water:
        sum_water += data

    avg_daily_elec = 0
    avg_daily_water = 0

    if daily_electric.rowcount is not 0:
	    avg_daily_elec = sum_elec / daily_electric.rowcount

    if daily_water.rowcount is not 0:
        avg_daily_water = sum_water / daily_water.rowcount

    return {
        'totals': {
            'electricity': sum_elec,
            'electricity_cost': kwh_to_dollars(sum_elec),
            'water': sum_water,
            'water_cost': gallons_to_dollars(sum_water)
        },
        'dailyaverage': {
            'electricity': avg_daily_elec,
            'water': avg_daily_water
        }
    }

def get_usage_month_range():
    earliest = db.engine.execute(f"select date from usage order by date asc limit 1;")
    latest = db.engine.execute(f"select date from usage order by date desc limit 1;")

    earliest_date = datetime.datetime.now()
    latest_date = datetime.datetime.now()

    if earliest.rowcount is not 0:
        return {
            'start': earliest.first()[0].isoformat(),
            'end': latest.first()[0].isoformat()
        }
    else:
        return {
            'start': earliest_date.isoformat(),
            'end': latest_date.isoformat()
        }  

def get_temperature_data(start: str):
        # Get start date as datetime
    startdt = datetime.datetime.strptime(start, '%Y-%m-%d')
    enddt = last_day_of_month(startdt) # Calculate last day of the current month

    # Convert back to ISO format for sql purposes
    start = startdt.strftime('%Y-%m-%d')
    end = enddt.strftime('%Y-%m-%d')

    exttemps = db.engine.execute(f"SELECT date_trunc('hour', date) as daterange, avg(temperature) FROM eventlog WHERE state = 'EXTTEMP' AND date BETWEEN '{start}' AND '{end}' GROUP BY 1 ORDER BY daterange ASC;")
    inttemps = db.engine.execute(f"SELECT date_trunc('hour', date) as daterange, avg(temperature) FROM eventlog WHERE state = 'INTTEMP' AND date BETWEEN '{start}' AND '{end}' GROUP BY 1 ORDER BY daterange ASC;")

    intraw = []
    extraw = []

    # Map electric data from raw sql tuples
    for date, data in inttemps:
        intraw.append([utc_to_local(date).strftime('%Y-%m-%d %H:%M:%S'), str(data)])

    # Map water data from raw sql tuples
    for date, data in exttemps:
        extraw.append([utc_to_local(date).strftime('%Y-%m-%d %H:%M:%S'), str(data)])

    return {
        'internal': intraw,
        'external': extraw
    }

def get_graphing_data(start: str):
    # Get start date as datetime
    startdt = datetime.datetime.strptime(start, '%Y-%m-%d')
    enddt = last_day_of_month(startdt) # Calculate last day of the current month

    # Convert back to ISO format for sql purposes
    start = startdt.strftime('%Y-%m-%d')
    end = enddt.strftime('%Y-%m-%d')

    daily_electric = db.engine.execute(f"SELECT date_trunc('day', date) as daterange, sum(data) FROM usage WHERE type = 'electric' AND date BETWEEN '{start}' AND '{end}' GROUP BY 1 ORDER BY daterange ASC;")
    daily_water = db.engine.execute(f"SELECT date_trunc('day', date) as daterange, sum(data) FROM usage WHERE type = 'water' AND date BETWEEN '{start}' AND '{end}' GROUP BY 1 ORDER BY daterange ASC;")

    # Keep running totals
    sum_elec = 0
    sum_water = 0

    # Raw values for sklearn purposes
    xvalselec = []
    yvalselec = []

    elecraw = []
    electots = []

    xvalswater = []
    yvalswater = []

    waterraw = []
    watertots = []

    # Counters
    ielec = 1
    iwater = 1

    # Map electric data from raw sql tuples
    for date, data in daily_electric:
        xvalselec.append(ielec)
        yvalselec.append(sum_elec)
        ielec += 1
        sum_elec += data
        elecraw.append([utc_to_local(date).strftime('%Y-%m-%d %H:%M:%S'), data])
        electots.append([utc_to_local(date).strftime('%Y-%m-%d %H:%M:%S'), sum_elec])

    # Map water data from raw sql tuples
    for date, data in daily_water:
        xvalswater.append(iwater)
        yvalswater.append(sum_water)
        iwater += 1
        sum_water += data
        waterraw.append([utc_to_local(date).strftime('%Y-%m-%d %H:%M:%S'), data])
        watertots.append([utc_to_local(date).strftime('%Y-%m-%d %H:%M:%S'), sum_water])


    # Get the number of the last day of current month
    end_day_num = enddt.day
    ey_month_end_prediction = 0
    wy_month_end_prediction = 0

    try:
        # Linear regression for electricity totals
        print("ELEC REGRESSION ======")
        ex = np.asarray(xvalselec).reshape((-1, 1))
        ey = np.asarray(yvalselec).reshape((-1, 1))
        elec_model = LinearRegression().fit(ex, ey)
        er_sq = elec_model.score(ex, ey)
        print('     coefficient of determination:', er_sq)

        ey_month_end_prediction = elec_model.predict(np.asarray([[end_day_num]]))[0][0]

        print('     elec eom prediction:', ey_month_end_prediction)

        # Linear regression for water totals\
        print("WATER REGRESSION ======")
        wx = np.asarray(xvalswater).reshape((-1, 1))
        wy = np.asarray(yvalswater).reshape((-1, 1))
        water_model = LinearRegression().fit(wx, wy)
        wr_sq = water_model.score(wx, wy)
        print('     coefficient of determination:', wr_sq)

        wy_month_end_prediction = water_model.predict(np.asarray([[end_day_num]]))[0][0]

        print('     water eom prediction:', wy_month_end_prediction)
    except:
        pass

    # Calculation of pricing
    # Electricity 0.12 per kWh
    # Water $2.52 per 100 Cubic Feet of water
    # 100 Cubic Feet is 748 Gallon
    


    return {
        'month_end_predict': {
            'electric': ey_month_end_prediction,
            'electric_cost': kwh_to_dollars(ey_month_end_prediction),
            'water': wy_month_end_prediction,
            'water_cost': gallons_to_dollars(wy_month_end_prediction)
        },
        'electric': {
            'raw': elecraw,
            'runningtotal': electots
        },
        'water': {
            'raw': waterraw,
            'runningtotal': watertots
        }
    }



