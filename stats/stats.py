
# coding: utf-8

# In[1]:

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

#print(df.groupby("agency_name").count().loc[:,['route_id']].sort_values(by='route_id'))

#print(df.groupby("stop_name").count().loc[:,['route_id']].sort_values(by='route_id'))

df = df.sort_values(by=['route_id','service_id', 'trip_id', 'direction_id', 'stop_sequence'], ascending=[True, True, True, True, True])


# In[13]:

#df.drop(['shape_id'],axis=1,inplace=True)
#'arrival_time', 'departure_time','pickup_type','drop_off_type''agency_id','agency_name','dobicek','promet''route_id','route_type','service_id','trip_id','direction_id','stop_id','stop_sequence'

df=df.drop_duplicates()
df


# In[55]:

from rtree import index
idx = index.Index()
left, bottom, right, top = (45, 13, 47, 15)
#idx.insert(0,(left,bottom,right,top))

tar = read('./data/google_feed/SI.csv')
for i in tar.index:
    idx.insert(i,(tar.X[i],tar.Y[i],tar.X[i],tar.Y[i]))
tar


# In[56]:

for i in range(df.shape[0]):
    left=df.iloc[i].stop_lat
    right=left
    bottom=df.iloc[i].stop_lon
    top=bottom
    tar.loc[list(idx.nearest((left,bottom,right,top),1))[0]:list(idx.nearest((left,bottom,right,top),1))[0],"SUM"]+=1
tar


# In[81]:

yay = read('./data/google_feed/yay.csv')
sums=yay["SUM"].tolist()
nmv=yay["NMV"].tolist()
pops=yay["POP"].tolist()
plt.plot(nmv,sums)
plt.xlabel("Nadmorska višina")
plt.ylabel("Število povezav")
plt.savefig('foo.png', bbox_inches='tight')
plt.show()


# In[76]:

plt.plot(pops,sums,"ro")
plt.xlabel("Število prebivalcev")
plt.ylabel("Število povezav")
plt.savefig('prebs.png', bbox_inches='tight')
plt.show()


# In[77]:

dif=[]
for i in range(len(sums)):
    dif.append(((sums[i]/47609)*100))
plt.plot(nmv,dif)
plt.xlabel("Nadmorska višina")
plt.ylabel("Število povezav v %")
plt.savefig('hei.png', bbox_inches='tight')
plt.show()


# In[80]:

sumy=2064000
test=[]
for i in range(len(sums)):
    test.append(((sums[i]/47609)*100)/((pops[i]/sumy)*100))
plt.plot(nmv,test)
plt.xlabel("Nadmorska višina")
plt.ylabel("Število povezav v %/število prebivalcev v %")
plt.savefig('hei.png', bbox_inches='tight')
plt.show()    


# In[ ]:



