import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import colorsys
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def read(location):
    return pd.read_csv(location)

def heatMapColorForValue(value):
  h = (1.0 - value) * 240
  return (h/360, 1, 0.5)

def getStopStyle(size):
    scale = 4
    size = size / 352
    h, s, v = heatMapColorForValue(min([size, 1]))
    color = colorsys.hsv_to_rgb(h, s, v)
    size = 1 + (size * scale) ** 1.1
    return (size, color)

def plot_stops(row):
    x, y = row.name
    x, y = m(x, y)
    size, color = getStopStyle(row['stop_id'])
    m.plot(x, y, 'o', markersize=size, color=color, alpha=0.3, markeredgewidth=0.0)

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

def legend(df, dpi, title):
    ax.text(200 * dpi, 35 * dpi, title, fontsize=8)
    stop_id = [0, 1, 2, 10, 20, int(len(df) * 0.02), int(len(df) * 0.1), len(df) - 1]
    items = sorted(set([df.stop_id[id] for id in stop_id if len(df) > id]))[::-1]
    y = 110
    step = 10
    for i, item in enumerate(items):
        size, color = getStopStyle(item)
        plt.plot(285 * dpi, y * dpi, 'o', markersize=size, color=color, alpha=0.3, markeredgewidth=0.0)
        ax.text(265 * dpi, (y - 1.7) * dpi, item, fontsize=5)
        y = y - (step + size / 2)


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
m = Basemap(resolution='c',  # c, l, i, h, f or None
            projection='merc',
            lat_0=46.161449, lon_0=14.997260,
            # westlimit=13.3319; southlimit=45.3946; eastlimit=16.6168; northlimit=46.9203
            llcrnrlon=13.3319, llcrnrlat=45.3946, urcrnrlon=16.6168, urcrnrlat=46.9203)
m.drawmapboundary(fill_color='#fefefe')

# draw Slovenian surface
ax = plt.gca()
shapes = m.readshapefile('../data/map/cn', 'borders', drawbounds=False)
patches   = []
for info, shape in zip(m.borders_info, m.borders):
    if info['CNTR_ID'] == 'SI':
        patches.append(Polygon(np.array(shape), True))
ax.add_collection(PatchCollection(patches, '-', color='#eeeeee', linewidths=0.1,))

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
m.plot(x_p, y_p, '-', markersize=0, linewidth=0.3, color='k', markerfacecolor='b', alpha=0.2)

group = df.groupby(['stop_lon','stop_lat']).count().sort_values(by='trip_id', ascending=False)
# draw stop stations
group.apply(plot_stops, axis=1)

dpi = 1200
legend(group, dpi, "Število prihodov \n na postajo")
plt.title("Zemljevid avtobusnih postaj in linij v Sloveniji")

# save map
plt.savefig("map.png", transparent=False, aspect='auto', bbox_inches='tight',dpi=dpi)
