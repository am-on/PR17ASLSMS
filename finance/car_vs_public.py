from datetime import datetime
import datetime as dt
import pandas as pd
import googlemaps


def read(location):
    return pd.read_csv(location)

#calculates distance and time between the given locations at the specified time
def calculate_time(start_lat, start_lon, dep_time, end_lat, end_lon, mode):
    time = datetime.strptime(date + ' ' + dep_time, '%d.%m.%Y %H:%M:%S')
    try:  # get directions from start to end at given time
        directions = gmaps.directions(origin=str(start_lat) + ',' + str(start_lon),
                                      destination=str(end_lat) + ',' + str(end_lon),
                                      mode=mode,
                                      departure_time=time)
    except:  # route doesn't exist
        return 0, 1
    try:  # get distance from data
        return (directions[0].get('legs')[0].get('distance').get('value') / 1000,
                int(directions[0].get('legs')[0].get('duration').get('value') / 60))  # distance (km), duration (min)
    except IndexError:  # bad data returned
        return 0, 1

#gets data for public transport and cars
def time(start_lat, start_lon, dep_time, end_lat, end_lon):
    fin = str(start_lat) + ' ' + str(start_lon) + ' ' + str(end_lat) + ' ' + str(end_lon)
    for elt in visited:  # check if we already have the distance saved from before
        if elt[0] == fin:
            return elt  # saved distance
    valC = calculate_time(start_lat, start_lon, dep_time, end_lat, end_lon, 'driving')  #car
    valT = calculate_time(start_lat, start_lon, dep_time, end_lat, end_lon, 'transit')  #public transport
    visited.insert(0, (fin, valC, valT))  # save calculation for later
    return fin, valC, valT


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

avgC = 0
avgT = 0
bestCvsT = None
sameCvsT = set()
worstCvsT = None
start_lat = None
start_lon = None
dep_time = None
end_lat = None
end_lon = None
i = 0
l = len(df.index) - 1
visited = []  # every duration already calculated
gmaps = googlemaps.Client(key='AIzaSyAjAw1bVBU1KncV-zg2RS9QrhbSAA_0aag')
date = dt.date.today() + dt.timedelta(days=1)
date = date.strftime('%d.%m.%Y')

#work while there's still data
while True:
    row = df[i:i + 1]
    if int(row['stop_sequence'].values[0]) == 1: #first stop in sequence; save starting location and time
        start_lat = float(row['stop_lat'].values[0])
        start_lon = float(row['stop_lon'].values[0])
        dep_time = row['departure_time'].values[0]
        i += 1
        continue
    elif i == l: #last stop in entire df
        end_lat = float(row['stop_lat'].values[0])
        end_lon = float(row['stop_lon'].values[0])
        fin, valC, valT = time(start_lat, start_lon, dep_time, end_lat, end_lon)
        try:
            ratioC = valC[0] / (valC[1] / 60)
            ratioT = valT[0] / (valT[1] / 60)
            ratio = ratioC / ratioT
        except ZeroDivisionError:
            ratioC = 0
            ratioT = 0
            ratio = None
        if ratioC != 0 and ratioT != 0:
            if bestCvsT is None or ratio > bestCvsT[0]:
                bestCvsT = (ratio, fin)
            if 0.95 < ratio < 1.05:
                sameCvsT.add(fin)
            if worstCvsT is None or ratio < worstCvsT[0]:
                worstCvsT = (ratio, fin)
            if avgC != 0:
                avgC += ratioC
                avgC /= 2
            else:
                avgC += ratioC

            if avgT != 0:
                avgT += ratioT
                avgT /= 2
            else:
                avgT += ratioT
        break
    if i < l and df.iloc[[i + 1]]['stop_sequence'].item() == 1: #last stop in sequence; calculate everything
        end_lat = float(row['stop_lat'].values[0])
        end_lon = float(row['stop_lon'].values[0])
        fin, valC, valT = time(start_lat, start_lon, dep_time, end_lat, end_lon)
        try: #can return 0 if route not found
            ratioC = valC[0] / (valC[1] / 60)
            ratioT = valT[0] / (valT[1] / 60)
            ratio = ratioC / ratioT
        except ZeroDivisionError:
            ratioC = 0
            ratioT = 0
            ratio = None
        if ratioC != 0 and ratioT != 0: #if data wasn't bad
            if bestCvsT is None or ratio > bestCvsT[0]:
                bestCvsT = (ratio, fin)
            if 0.95 < ratio < 1.05:
                sameCvsT.add(fin)
            if worstCvsT is None or ratio < worstCvsT[0]:
                worstCvsT = (ratio, fin)
            if avgC != 0:
                avgC += ratioC
                avgC /= 2
            else:
                avgC += ratioC

            if avgT != 0:
                avgT += ratioT
                avgT /= 2
            else:
                avgT += ratioT
    i += 1
#print results
print(bestCvsT)
print(sameCvsT)
print(worstCvsT)
print(avgC)
print(avgT)