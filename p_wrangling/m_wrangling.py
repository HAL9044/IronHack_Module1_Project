import pandas as pd
from shapely.geometry import Point
import geopandas as gpd  
   

def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between to latitude/longitude pair point in degrees (i.e.: 40.392436 / -3.6994487)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish)
#Selects columns from raw dataframes when imported from API and database
def dframe_col_selector (emba_dframe, bike_dframe):
    LONGITUDE = []
    LATITUDE = []
    for i in range(len(bike_dframe['geometry_coordinates'])):
        LONGITUDE.append(float(bike_dframe['geometry_coordinates'][i].split(",")[0].replace("[", "")))
        LATITUDE.append(float(bike_dframe['geometry_coordinates'][i].split(",")[1].replace("]", "")))   

    bike_dframe = bike_dframe[['id', 'name', 'address']]
    bike_dframe['LATITUDE'] = LATITUDE
    bike_dframe['LONGITUDE'] = LONGITUDE
    emba_dframe = emba_dframe[['NOMBRE', 'DISTRITO', 'BARRIO', 'CLASE-VIAL', 'NOMBRE-VIA', 'NUM', 'PLANTA', 'PUERTA','LATITUD', 'LONGITUD']]
    return (emba_dframe, bike_dframe)
#Chops dataframe to simplify calculating process
def dframe_chopper (long, lat, dataframe, i):
    check = False
    long_up = long 
    long_low = long
    lat_up = lat
    lat_low = lat
    
    while check == False:
        dframe = dataframe
        i += 1
        long_up += (0.001 * i) 
        long_low -= (0.001 * i)
        lat_up += (0.001 * i)
        lat_low -= (0.001 * i)
        dframe = dframe[dframe.LONGITUDE >= long_low]
        dframe = dframe[dframe.LONGITUDE <= long_up]
        dframe = dframe[dframe.LATITUDE >= lat_low]
        dframe = dframe[dframe.LATITUDE <= lat_up]
        
        if len(dframe) != 0:
            check = True
        
    return (dframe, i)


