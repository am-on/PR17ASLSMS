import pandas as pd
import matplotlib.pyplot as plt
import colorsys
from mpl_toolkits.basemap import Basemap

def read(location):
    return pd.read_csv(location)

def heatMapColorforValue(value):
  h = (1.0 - value) * 240
  return (h/360, 1, 0.5)

def plot_stops(row):
    scale = 15
    x, y = row.name
    x, y = m(x, y)
    size = row['stop_id'] / 352
    h, s, v = heatMapColorforValue(min([size, 1]))
    color = colorsys.hsv_to_rgb(h, s, v)
    size = min([5+(size*scale)**1.2, 120])
    m.plot(x, y, 'o', markersize=size, color=color, alpha=0.3)

def lines(row):
    global before
    global x_p
    global y_p

    a = str(row['trip_id'])
    b = str(before['trip_id'])

    if  a == b:
        x1, y1 = before['stop_lon'], before['stop_lat']
        x2, y2 = row['stop_lon'], row['stop_lat']
        x0, y0 = m([x1, x2], [y1, y2])
        x_p.extend(x0)
        y_p.extend(y0)
        x_p.append(None)
        y_p.append(None)

    before = row.copy()


# read data, drop unnecessary cols
agency = read('../data/google_feed/agency.txt')
agency.drop(['agency_url', 'agency_timezone', 'agency_phone', 'agency_lang'],axis=1,inplace=True)

routes = read('../data/google_feed/routes.txt')
routes.drop(['route_short_name', 'route_desc', 'route_url', 'route_color', 'route_text_color'],axis=1,inplace=True)

trips = read('../data/google_feed/trips.txt')
trips.drop(['trip_headsign', 'block_id'],axis=1,inplace=True)

stopTimes = read('../data/google_feed/stop_times.txt')
stopTimes.drop(['stop_headsign'],axis=1,inplace=True)

stops = read('../data/google_feed/stops.txt')
stops.drop(['stop_desc', 'zone_id', 'stop_url'],axis=1,inplace=True)

# road shapes, might use instead of direct lines
# shapes = read('./data/google_feed/shapes.txt')

# merge data into one df
df = pd.merge(agency, routes, on='agency_id')
df = pd.merge(df, trips, on='route_id')
df = pd.merge(df, stopTimes, on='trip_id')
df = pd.merge(df, stops, on='stop_id')

# create map
fig, ax = plt.subplots(figsize=(40,80))
m = Basemap(resolution='f',  # c, l, i, h, f or None
            projection='merc',
            lat_0=46.161449, lon_0=14.997260,
            # westlimit=13.3319; southlimit=45.3946; eastlimit=16.6168; northlimit=46.9203
            llcrnrlon=13.3319, llcrnrlat=45.3946, urcrnrlon=16.6168, urcrnrlat=46.9203)
m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
m.drawcoastlines()

# sort by route and stop sequence
df = df.sort_values(by=['route_id','service_id', 'trip_id', 'direction_id', 'stop_sequence'],
                    ascending=[True, True, True, True,True])

# global vars, for speeding up line drawing
# http://exnumerus.blogspot.si/2011/02/how-to-quickly-plot-multiple-line.html
before = df[:1]
x_p = []
y_p = []
df[2:].apply(lines, axis=1)
# draw lines
m.plot(x_p, y_p, '-', markersize=0, linewidth=1, color='k', markerfacecolor='b', alpha=0.2)

group = df.groupby(['stop_lon','stop_lat']).count().sort_values(by='trip_id', ascending=False)
#draw stop stations
group.apply(plot_stops, axis=1)

# save map
plt.savefig("map.png")
