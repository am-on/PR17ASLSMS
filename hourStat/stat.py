import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

from map.map import Map

rcParams.update({'figure.autolayout': True})

def read(location):
    return pd.read_csv(location)

def toTime(time):
    fixedTime = []
    # fix invalid time entries
    for t in time:
        if t[:2] == '24':
            t = '00' + t[2:]
        elif t[:2] == '25':
            t = '01' + t[2:]
        fixedTime.append(t)

    # convert to pd datetime
    return pd.to_datetime(fixedTime)

def getStats(df):

    def topStops(row):
        stopDetails = stops[stops.stop_name == row.name]
        print("{0} (lat: {1}, lo: {2}) | število postankov: {3}".format(row.name, stopDetails.stop_lat.values[0], stopDetails.stop_lon.values[0], row.values[0]))

    routeN = len(df.groupby('route_id'))
    uniqueStopsN = len(df.groupby('stop_id'))
    stopsN = len(df)

    print("Število aktivnih linij: {0}, \n"
          "število postaj {1}, \n"
          "število postankov: {2},\n"
          "povprečno število postankov na postajo: {3}".format(routeN, uniqueStopsN, stopsN, int(stopsN/uniqueStopsN) if uniqueStopsN > 0 else 0))
    print()
    df.groupby("stop_name").count().loc[:,['route_id']].sort_values(by='route_id', ascending=False)[:10].apply(topStops, axis=1)

    return ({"routes": routeN, "unique_stops": uniqueStopsN, "stops": stopsN})

# read data, drop unnecessary cols
agency = read('../data/google_feed/agency.txt')
agency.drop(['agency_url', 'agency_timezone', 'agency_phone', 'agency_lang'],axis=1,inplace=True)

routes = read('../data/google_feed/routes.txt')
routes.drop(['route_short_name', 'route_desc', 'route_url', 'route_color', 'route_text_color'],axis=1,inplace=True)

trips = read('../data/google_feed/trips.txt')
trips.drop(['trip_headsign', 'block_id'],axis=1,inplace=True)

stopTimes = read('../data/google_feed/stop_times.txt')
stopTimes.drop(['stop_headsign'],axis=1,inplace=True)
stopTimes.arrival_time = toTime(stopTimes.arrival_time)
stopTimes.departure_time = toTime(stopTimes.departure_time)

stops = read('../data/google_feed/stops.txt')
stops.drop(['stop_desc', 'zone_id', 'stop_url'],axis=1,inplace=True)

# merge data into one df
df = pd.merge(agency, routes, on='agency_id')
df = pd.merge(df, trips, on='route_id')

df = pd.merge(df, stopTimes, on='trip_id')
df = pd.merge(df, stops, on='stop_id')

df = df.sort_values(by=['route_id','service_id', 'trip_id', 'direction_id', 'stop_sequence'], ascending=[True, True, True, True, True])

# get daily stats
getStats(df)

# create time ranges
startHourRange = pd.date_range(start='00:00:00', periods=24, freq=pd.offsets.Hour(n=1))
stopHourRange = pd.date_range(start='00:59:59', periods=24, freq=pd.offsets.Hour(n=1))
#startHourRange = pd.date_range(start='01:00:00', periods=1, freq=pd.offsets.Hour(n=1))
#stopHourRange = pd.date_range(start='03:59:59', periods=1, freq=pd.offsets.Hour(n=1))
hourRange = zip(startHourRange, stopHourRange)

freq = []
time = []
for start, stop in hourRange:
    f = df[(df.arrival_time >= start) & (df.arrival_time < stop)]

    freq.append(len(f))
    timeLabel = start.strftime('%H:%M:%S') + ' - ' + stop.strftime('%H:%M:%S')
    time.append(timeLabel)

    # draw map
    #Map(f, title="med " + timeLabel, filename=timeLabel)

    print("\n \n \nStatistika za: " + time[-1:][0] + "\n")
    getStats(f)


freqDf = pd.DataFrame(data=freq, index=time, columns=['Število prihodov',])

plt.figure()
plt.title("Število avtobusnih prihodov po urah")
freqDf.plot(kind='bar')
plt.savefig("hourBarPlot.png")
plt.close()


