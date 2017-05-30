from datetime import datetime
from collections import defaultdict
import datetime as dt
import pandas as pd
import googlemaps


def read(location):
    return pd.read_csv(location)

#calculates distance between two points on map at the given time
def calculate_dist(start_lat, start_lon, dep_time, end_lat, end_lon):
    time = datetime.strptime(date + ' ' + dep_time, '%d.%m.%Y %H:%M:%S')
    try:  # get directions from start to end at given time
        directions = gmaps.directions(origin=str(start_lat) + ',' + str(start_lon),
                                      destination=str(end_lat) + ',' + str(end_lon),
                                      mode="transit",
                                      departure_time=time)
    except:  # route doesn't exist
        return 0
    try:  # get distance from data
        return directions[0].get('legs')[0].get('distance').get('value') / 1000
    except IndexError:  # bad data returned
        return 0

#checks if distance was already calculated or calculates it and saves it for later
def distance(start_lat, start_lon, dep_time, end_lat, end_lon):
    fin = str(start_lat) + ' ' + str(start_lon) + ' ' + str(end_lat) + ' ' + str(end_lon)
    for elt in visited:  # check if we already have the distance saved from before
        if elt[0] == fin:
            return elt[1]  # saved distance
    dist = calculate_dist(start_lat, start_lon, dep_time, end_lat, end_lon)  # calculate distance
    visited.insert(0, (fin, dist))  # save calculation for later
    return dist


# read data, drop unnecessary cols
agency = read('./data/google_feed/agency.txt')
agency.drop(['agency_name', 'agency_url', 'agency_timezone', 'agency_phone', 'agency_lang'],
            axis=1, inplace=True)
routes = read('./data/google_feed/routes.txt')
routes.drop(['route_short_name', 'route_long_name', 'route_desc', 'route_type', 'route_url', 'route_color',
             'route_text_color'], axis=1, inplace=True)
trips = read('./data/google_feed/trips.txt')
trips.drop(['trip_headsign', 'block_id', 'shape_id'], axis=1, inplace=True)
stopTimes = read('./data/google_feed/stop_times.txt')
stopTimes.drop(['stop_headsign', 'pickup_type', 'drop_off_type'], axis=1, inplace=True)
stops = read('./data/google_feed/stops.txt')
stops.drop(['stop_name', 'stop_desc', 'zone_id', 'stop_url'], axis=1, inplace=True)
# merge data into one df
df = pd.merge(agency, routes, on='agency_id')
df = pd.merge(df, trips, on='route_id')
df = pd.merge(df, stopTimes, on='trip_id')
df = pd.merge(df, stops, on='stop_id')
df = df.sort_values(by=['agency_id', 'route_id', 'service_id', 'trip_id', 'direction_id', 'stop_sequence'],
                    ascending=[True, True, True, True, True, True])

start_lat = None
start_lon = None
dep_time = None
end_lat = None
end_lon = None
i = 0
l = len(df.index) - 1
visited = []  # every distance already calculated
gmaps = googlemaps.Client(key='AIzaSyAjAw1bVBU1KncV-zg2RS9QrhbSAA_0aag')
date = dt.date.today().strftime('%d.%m.%Y')
d = defaultdict(int) #distance dict
n = defaultdict(int) #number of routes dict

while True:
    row = df[i:i + 1]
    if int(row['stop_sequence'].values[0]) == 1: #first stop in sequence
        start_lat = float(row['stop_lat'].values[0])
        start_lon = float(row['stop_lon'].values[0])
        dep_time = row['departure_time'].values[0]
        i += 1
        continue
    elif i == l: #last stop in df
        end_lat = float(row['stop_lat'].values[0])
        end_lon = float(row['stop_lon'].values[0])
        dist = distance(start_lat, start_lon, dep_time, end_lat, end_lon)
        d[row['agency_id'].values[0]] += dist
        n[row['agency_id'].values[0]] += 1
        break
    if i < l and df.iloc[[i + 1]]['stop_sequence'].item() == 1: #last stop in sequence
        end_lat = float(row['stop_lat'].values[0])
        end_lon = float(row['stop_lon'].values[0])
        dist = distance(start_lat, start_lon, dep_time, end_lat, end_lon)
        d[row['agency_id'].values[0]] += dist
        n[row['agency_id'].values[0]] += 1
    i += 1
#print data
print(dict(d))
print(dict(n))
