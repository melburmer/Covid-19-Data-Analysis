# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:28:32 2020

@author: Pc
"""

import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px


df = pd.read_csv(r"dataset\time_series_covid_19_confirmed.csv")

df.head()
###################
# all world

total_confirmed = df.groupby('Country/Region')['3/14/20'].sum()

total_confirmed = pd.DataFrame(data=total_confirmed,index=total_confirmed.index)

total_confirmed.columns = ["Total Confirmed"]

total_confirmed.sort_values("Total Confirmed",axis=0,inplace=True,ascending=False)

total_confirmed.head()  # top five

# ilk 10 ülkeyi görselleştirelim

ax1 = total_confirmed[0:10].plot(kind="barh",colormap="Set1",width=0.7,stacked=True)
ax1.set_title("Top 10 Confirmed Count by Country",fontweight="bold")
ax1.set_xlabel("Total Confirmed")

for p in ax1.patches:
    left, bottom, width, height = p.get_bbox().bounds
    if(width<600):
        ax1.annotate(str(int(width)), xy=(left+4*width, bottom+height/2),ha='center', va='center',fontweight="bold")
    else:
        ax1.annotate(str(int(width)), xy=(left+width/2, bottom+height/2),ha='center', va='center',fontweight="bold")

#China
china_confirmed = df[df["Country/Region"]=="China"]


td_byprovince_china = pd.DataFrame(china_confirmed.groupby("Province/State").sum()['3/14/20'])
td_byprovince_china.columns = ["Total Recovered"]
td_byprovince_china.sort_values("Total Recovered",ascending=False,inplace=True)
td_byprovince_china.head()  # Çin'de en fazla 5 ölüm



china_confirmed = china_confirmed.groupby("Country/Region").sum()

china_confirmed.drop(["Lat","Long"],axis=1,inplace=True)

china_confirmed =china_confirmed.T
# data is cumulative now

china_confirmed_noncum = china_confirmed.diff()

china_confirmed_noncum.drop("1/22/20",axis=0,inplace=True)

# görselleştirme

fig = go.Figure(layout=go.Layout(title=go.layout.Title(text="Çin Ölüm Sayıları")))

fig.add_trace(go.Scatter(x=china_confirmed_noncum.index, y=china_confirmed_noncum["China"], mode='lines',
        name="deneme",
        line=dict(color='rgb(0,128,0)', width=3),
        connectgaps=True))

fig.update_layout(
    autosize=True,
    width=900,
    height=600,
 
)

fig.show()

########
# Usa

usa = df[df["Country/Region"]=="US"]
usa.drop("Country/Region",axis=1,inplace=True)

td_byprovince_usa = pd.DataFrame(usa.groupby("Province/State").sum()['3/14/20'])
td_byprovince_usa.columns = ["Total Confirmed"]
td_byprovince_usa.sort_values("Total Confirmed",ascending=False,inplace=True)
td_byprovince_usa.head()  # Usa'da en fazla 5 tedavi

###### plot

usa_confirmed = df[df["Country/Region"]=="US"]

usa_confirmed = usa_confirmed.groupby("Country/Region").sum()

usa_confirmed.drop(["Lat","Long"],axis=1,inplace=True)

usa_confirmed = usa_confirmed.T
# data is cumulative now

usa_recovered_noncum = usa_confirmed.diff()  # cumulatif değil artık

usa_recovered_noncum.drop("1/22/20",axis=0,inplace=True)



usa_recovered_noncum.plot()

# Italy
italy = df[df["Country/Region"]=="Italy"]
italy.drop("Country/Region",axis=1,inplace=True)

print("Italy Total Cases:" + str(italy["3/14/20"].values))
###### plot

italy_confirmed = df[df["Country/Region"]=="Italy"]

italy_confirmed = italy_confirmed.groupby("Country/Region").sum()

italy_confirmed.drop(["Lat","Long"],axis=1,inplace=True)

italy_confirmed = italy_confirmed.T
# data is cumulative now

italy_confirmed_noncum = italy_confirmed.diff()  # cumulatif değil artık

italy_confirmed_noncum.drop("1/22/20",axis=0,inplace=True)



italy_confirmed_noncum.plot()

# DÜNYADAKİ TÜM onaylanan vakalar


df.drop([104,105],axis=0,inplace=True) # dublike kayıtlar


df["Province/State"].fillna(df["Country/Region"],inplace=True)

total_confirmed = pd.DataFrame(df.groupby(["Country/Region",'Province/State'])['3/14/20'].sum())

total_confirmed.columns = ["Total Confirmed"]

total_confirmed["Lat"] = np.nan
total_confirmed["Long"] = np.nan



for loc in total_confirmed.index:
    
    temp = df[(df["Country/Region"] == loc[0]) & (df["Province/State"]== loc[1])]
    total_confirmed["Lat"][loc] = temp["Lat"]
    total_confirmed["Long"][loc] = temp["Long"]


total_confirmed = total_confirmed[total_confirmed["Total Confirmed"]>0]     
 
fig = px.density_mapbox(total_confirmed, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name=total_confirmed.index.get_level_values(1), 
                        hover_data=["Total Confirmed"], 
                        color_continuous_scale="Portland",
                        radius=7, 
                        zoom=0,height=500)    
fig.update_layout(title="World Wide Corona Virus Cases Confirmed",
                  font=dict(family="Courier New, monospace",
                            size=18,
                            color="#7f7f7f")
                 )
fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=0)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()