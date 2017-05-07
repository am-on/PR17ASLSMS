from datetime import datetime
from collections import defaultdict
import datetime as dt
import pandas as pd
import googlemaps
import json


def read(location):
    return pd.read_csv(location)


def calculate_dist(start_lat, start_lon, dep_time, end_lat, end_lon):
    time = datetime.strptime(date+' '+dep_time, '%d.%m.%Y %H:%M:%S')
    #print(str(start_lat)+' '+str(start_lon)+' '+str(time)+' '+str(end_lat)+' '+str(end_lon))
    try:
        directions = gmaps.directions(origin=str(start_lat)+','+str(start_lon),
                                         destination=str(end_lat)+' '+str(end_lon),
                                         mode="transit",
                                         departure_time=time)
    except:
        return 0
    #print(directions)
    #print(directions[0])
    #print(directions[0].keys())
    #print(directions[0].get('legs')[0].keys())
    try:
        return directions[0].get('legs')[0].get('distance').get('value')
    except IndexError:
        print("ERR(directions):"+str(directions))
        return 0
    #print(directions[0].get('distance'))
    #return directions

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

# road shapes, might use instead of direct lines
# shapes = read('./data/google_feed/shapes.txt')

# merge data into one df
df = pd.merge(agency, routes, on='agency_id')
df = pd.merge(df, trips, on='route_id')
df = pd.merge(df, stopTimes, on='trip_id')
df = pd.merge(df, stops, on='stop_id')

df = df.sort_values(by=['agency_id', 'route_id', 'service_id', 'trip_id', 'direction_id', 'stop_sequence'],
                    ascending=[True, True, True, True, True, True])
"""print(df[0:45])
writer=pd.ExcelWriter("izvoz.xlsx", engine="xlsxwriter")
df.to_excel(writer, sheet_name='Sheet1')
writer.save()"""
start_lat=None
start_lon=None
dep_time=None
end_lat=None
end_lon=None
i=0
l=len(df.index)-1
print(l)
visited=[] #every distance already calculated
gmaps = googlemaps.Client(key='AIzaSyAjAw1bVBU1KncV-zg2RS9QrhbSAA_0aag')
date=dt.date.today().strftime('%d.%m.%Y')
d=defaultdict(int)
n=defaultdict(int)
while True:
    row=df[i:i+1]
    #print(row['stop_sequence'].values[0])
    #print(df[i:i+1]['stop_sequence'].values[0])
    #if df.iloc[[i]]['stop_sequence'].item()==1:
    if int(df[i:i+1]['stop_sequence'].values[0])==1:
        print("T1")
        start_lat=float(row['stop_lat'].values[0])
        start_lon=float(row['stop_lon'].values[0])
        dep_time=row['arrival_time'].values[0]
        i+=1
        continue
    elif i==l:
        end_lat = float(row['stop_lat'].values[0])
        end_lon = float(row['stop_lon'].values[0])
        fin=str(start_lat)+' '+str(start_lon)+' '+str(end_lat)+' '+str(end_lon)
        vis=False
        for elt in visited:
            if elt[0]==fin:
                if elt[1]==0:
                    dist=calculate_dist(start_lat, start_lon, dep_time, end_lat, end_lon)
                    visited.remove(elt)
                    visited.insert(0, (fin, dist))
                d[row['agency_id'].values[0]]+=elt[1]
                n[row['agency_id'].values[0]] += 1
                vis=True
                break
        if vis==False:
            print('to_calc')
            dist=calculate_dist(start_lat, start_lon, dep_time, end_lat, end_lon)
            visited.insert(0,(fin,dist))
            d[row['agency_id'].values[0]] += dist
            n[row['agency_id'].values[0]] += 1
        break
    if i<l and df.iloc[[i+1]]['stop_sequence'].item()==1:
        print("T2")
        end_lat=float(row['stop_lat'].values[0])
        end_lon=float(row['stop_lon'].values[0])
        #print('to_calc')
        #print(str(start_lat)+" "+str(start_lon)+" "+str(dep_time)+" "+str(end_lat)+" "+str(end_lon))
        #d[row['agency_id'].values[0]] += calculate_dist(start_lat, start_lon, dep_time, end_lat, end_lon)
        fin = str(start_lat) + ' ' + str(start_lon) + ' ' + str(end_lat) + ' ' + str(end_lon)
        vis = False
        for elt in visited:
            if elt[0] == fin:
                if elt[1] == 0:
                    dist = calculate_dist(start_lat, start_lon, dep_time, end_lat, end_lon)
                    visited.remove(elt)
                    visited.insert(0,(fin, dist))
                d[row['agency_id'].values[0]] += elt[1]
                n[row['agency_id'].values[0]] += 1
                vis = True
                break
        if vis == False:
            print('to_calc')
            dist = calculate_dist(start_lat, start_lon, dep_time, end_lat, end_lon)
            visited.insert(0, (fin, dist))
            print(str(start_lat) + ' ' + str(start_lon) + ' ' + dep_time + ' ' + str(end_lat) + ' ' + str(end_lon))
            d[row['agency_id'].values[0]] += dist
            n[row['agency_id'].values[0]] += 1
        print(dict(d))
        print(dict(n))
        print(i)
    i+=1
print(dict(d))
print(dict(n))