# HomeIOT Data Generator

Here we will perform our data generation scripts that will interface with the database DAO objects to help aid in generating data.

## Running The Generator

```bash
# Must run with python3.6 or higher
python3 generate.py
```
## Required Dependency for weather_data.py

To run `weather_data.py`, there are various dependency that you might need to install if they are not installed.
```
geopy
darkskylib 0.3.91
```
## Before runnig weather_data.py
Just make sure to change this and give the key that is in your darksky account. If you cannot find it just press `console` 
and the it will be under `your secret key`.
```
key = "Add the API key of darksky here"
```  





## Running weather_data.py
To get the weather data of a city or a place, we need to create an instancte of class name Location with two attributes city name and state name. 
After the instance is created we can call `latitude`, `longitude`, `one_day_temp` and `one_hour_temp` functions upon the instance to get data.
There is also a method by which we can change the city without creating a whole new instance.

