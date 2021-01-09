# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 19:42:28 2020

@author: Pc
"""

import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px


df = pd.read_csv(r"dataset\time_series_covid_19_recovered.csv")

df.head()
###################
# all world

total_recovered = df.groupby('Country/Region')['3/14/20'].sum()

total_recovered = pd.DataFrame(data=total_recovered,index=total_recovered.index)

total_recovered.columns = ["Total Recovered"]

total_recovered.sort_values("Total Recovered",axis=0,inplace=True,ascending=False)

total_recovered.head()  # top five

# ilk 10 ülkeyi görselleştirelim

ax1 = total_recovered[0:10].plot(kind="barh",colormap="Set1",width=0.7,stacked=True)
ax1.set_title("Top 10 Recovered Count by Country",fontweight="bold")
ax1.set_xlabel("Total Recovered")

for p in ax1.patches:
    left, bottom, width, height = p.get_bbox().bounds
    if(width<600):
        ax1.annotate(str(int(width)), xy=(left+4*width, bottom+height/2),ha='center', va='center',fontweight="bold")
    else:
        ax1.annotate(str(int(width)), xy=(left+width/2, bottom+height/2),ha='center', va='center',fontweight="bold")

#China
china_recovered = df[df["Country/Region"]=="China"]



td_byprovince_china = pd.DataFrame(china_recovered.groupby("Province/State").sum()['3/14/20'])
td_byprovince_china.columns = ["Total Recovered"]
td_byprovince_china.sort_values("Total Recovered",ascending=False,inplace=True)
td_byprovince_china.head()  # Çin'de en fazla 5 ölüm



china_recovered = china_recovered.groupby("Country/Region").sum()

china_recovered.drop(["Lat","Long"],axis=1,inplace=True)

china_recovered =china_recovered.T
# data is cumulative now

china_recovered_noncum = china_recovered.diff()

china_recovered_noncum.drop("1/22/20",axis=0,inplace=True)

# görselleştirme

fig = go.Figure(layout=go.Layout(title=go.layout.Title(text="Çin Ölüm Sayıları")))

fig.add_trace(go.Scatter(x=china_recovered_noncum.index, y=china_recovered_noncum["China"], mode='lines',
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
td_byprovince_usa.columns = ["Total Recovered"]
td_byprovince_usa.sort_values("Total Recovered",ascending=False,inplace=True)
td_byprovince_usa.head()  # Usa'da en fazla 5 tedavi

###### plot

usa_recovered = df[df["Country/Region"]=="US"]

usa_recovered = usa_recovered.groupby("Country/Region").sum()

usa_recovered.drop(["Lat","Long"],axis=1,inplace=True)

usa_recovered = usa_recovered.T
# data is cumulative now

usa_recovered_noncum = usa_recovered.diff()  # cumulatif değil artık

usa_recovered_noncum.drop("1/22/20",axis=0,inplace=True)



usa_recovered_noncum.plot()


# DÜNYADAKİ TÜM İyileşmeler


df.drop([104,105],axis=0,inplace=True) # dublike kayıtlar 

df["Province/State"].fillna(df["Country/Region"],inplace=True)

total_recovered = pd.DataFrame(df.groupby(["Country/Region",'Province/State'])['3/14/20'].sum())

total_recovered.columns = ["Total Recovored"]

total_recovered["Lat"] = np.nan
total_recovered["Long"] = np.nan


for loc in total_recovered.index:
    temp = df[(df["Country/Region"] == loc[0]) & (df["Province/State"]== loc[1])]
    total_recovered["Lat"][loc] = temp["Lat"]
    total_recovered["Long"][loc] = temp["Long"]


total_recovered = total_recovered[total_recovered["Total Recovored"]>0]     
 
fig = px.density_mapbox(total_recovered, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name=total_recovered.index.get_level_values(1), 
                        hover_data=["Total Recovered"], 
                        color_continuous_scale="Portland",
                        radius=7, 
                        zoom=0,height=500)    
fig.update_layout(title="World Wide Corona Virus Cases Deaths",
                  font=dict(family="Courier New, monospace",
                            size=18,
                            color="#7f7f7f")
                 )
fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=0)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()





