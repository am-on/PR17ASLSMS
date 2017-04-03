import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read(location):
    return pd.read_csv(location)

# read data, drop unnecessary cols
agency = read('./data/google_feed/agency.txt')
agency.drop(['agency_url', 'agency_timezone', 'agency_phone', 'agency_lang'],axis=1,inplace=True)

routes = read('./data/google_feed/routes.txt')
routes.drop(['route_short_name', 'route_desc', 'route_url', 'route_color', 'route_text_color'],axis=1,inplace=True)

trips = read('./data/google_feed/trips.txt')
trips.drop(['trip_headsign', 'block_id'],axis=1,inplace=True)

stopTimes = read('./data/google_feed/stop_times.txt')
stopTimes.drop(['stop_headsign'],axis=1,inplace=True)

stops = read('./data/google_feed/stops.txt')
stops.drop(['stop_desc', 'zone_id', 'stop_url'],axis=1,inplace=True)

# merge data into one df
df = pd.merge(agency, routes, on='agency_id')
df = pd.merge(df, trips, on='route_id')
df = pd.merge(df, stopTimes, on='trip_id')
df = pd.merge(df, stops, on='stop_id')


print(agency)

#print(df.groupby("agency_name").count().loc[:,['route_id']].sort_values(by='route_id'))

#print(df.groupby("stop_name").count().loc[:,['route_id']].sort_values(by='route_id'))

#print(df.info())