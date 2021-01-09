# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 13:27:16 2020

@author: Pc
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#### TİME SERİES COVİD DEATHS ANALYSİS

df = pd.read_csv(r"dataset\time_series_covid_19_deaths.csv")

df.head()  # ilk ölümler

df.tail() # son ölümler

df.columns

# ülkelere göre toplam ölüm sayıları

total_deaths = df.groupby('Country/Region')['3/14/20'].sum()

total_deaths = pd.DataFrame(data=total_deaths,index=total_deaths.index)

total_deaths.columns = ["Total Deaths"]

total_deaths.sort_values("Total Deaths",axis=0,inplace=True,ascending=False)

total_deaths.head()  # top five

# ilk 10 ülkeyi görselleştirelim

ax1 = total_deaths[0:10].plot(kind="barh",colormap="Set1",width=0.7,stacked=True)
ax1.set_title("Top 10 Death Count by Country",fontweight="bold")
ax1.set_xlabel("Total Deaths")

for p in ax1.patches:
    left, bottom, width, height = p.get_bbox().bounds
    if(width<50):
        ax1.annotate(str(int(width)), xy=(left+3*width, bottom+height/2),ha='center', va='center',fontweight="bold")
    else:
        ax1.annotate(str(int(width)), xy=(left+width/2, bottom+height/2),ha='center', va='center',fontweight="bold")


# ülkeye özel analiz
#######################

# Çin

china = df[df["Country/Region"]=="China"]
china.columns

china.drop("Country/Region",axis=1,inplace=True)

td_byprovince_china = pd.DataFrame(china.groupby("Province/State").sum()['3/14/20'])
td_byprovince_china.columns = ["Total Deaths"]
td_byprovince_china.sort_values("Total Deaths",ascending=False,inplace=True)
td_byprovince_china.head()  # Çin'de en fazla 5 ölüm

# Ölüm sayılarının çizdirilmesi
############ plot

china_death = df[df["Country/Region"]=="China"]

china_death  = china_death .groupby("Country/Region").sum()

china_death .drop(["Lat","Long"],axis=1,inplace=True)

china_death  =china_death .T
# data is cumulative now

china_death_noncum = china_death.diff()  # cumulatif değil artık

china_death_noncum.drop("1/22/20",axis=0,inplace=True)

# görselleştirme

fig = go.Figure(layout=go.Layout(title=go.layout.Title(text="Çin Ölüm Sayıları")))

fig.add_trace(go.Scatter(x=china_death_noncum.index, y=china_death_noncum["China"], mode='lines',
        name="deneme",
        line=dict(color='rgb(0,128,0)', width=3),
        connectgaps=True))

fig.update_layout(
    autosize=True,
    width=900,
    height=600,
 
)

fig.show()

#######################

# USA

usa = df[df["Country/Region"]=="US"]
usa.drop("Country/Region",axis=1,inplace=True)


td_byprovince_usa = pd.DataFrame(usa.groupby("Province/State").sum()['3/14/20'])
td_byprovince_usa.columns = ["Total Deaths"]
td_byprovince_usa.sort_values("Total Deaths",ascending=False,inplace=True)
td_byprovince_usa.head()  # Usa'da en fazla 5 ölüm


usa_death = df[df["Country/Region"]=="China"]

usa_death = usa_death .groupby("Country/Region").sum()

usa_death.drop(["Lat","Long"],axis=1,inplace=True)

usa_death = usa_death .T
# data is cumulative now

usa_death_noncum = usa_death.diff()  # cumulatif değil artık

usa_death_noncum.drop("1/22/20",axis=0,inplace=True)

# görselleştirme

fig = go.Figure(layout=go.Layout(title=go.layout.Title(text="Çin Ölüm Sayıları")))

fig.add_trace(go.Scatter(x=usa_death_noncum.index, y=china_death_noncum["Us"], mode='lines',
        name="deneme",
        line=dict(color='rgb(0,128,0)', width=3),
        connectgaps=True))

fig.update_layout(
    autosize=True,
    width=900,
    height=600,
 
)

fig.show()


#######################
# DÜNYADAKİ TÜM ÖLÜMLER


df.drop([104,105],axis=0,inplace=True) # dublike kayıtlar

df["Province/State"].fillna(df["Country/Region"],inplace=True) 

total_deaths = pd.DataFrame(df.groupby(["Country/Region",'Province/State'])['3/14/20'].sum())

total_deaths.columns = ["Total Deaths"]

total_deaths["Lat"] = np.nan
total_deaths["Long"] = np.nan


for loc in total_deaths.index:
    temp = df[(df["Country/Region"] == loc[0]) & (df["Province/State"]== loc[1])]
    total_deaths["Lat"][loc] = temp["Lat"]
    total_deaths["Long"][loc] = temp["Long"]


total_deaths = total_deaths[total_deaths["Total Deaths"]>0]      
fig = px.density_mapbox(total_deaths, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name=total_deaths.index.get_level_values(1), 
                        hover_data=["Total Deaths"], 
                        color_continuous_scale="Portland",
                        radius=10, 
                        zoom=0,height=700)    
fig.update_layout(title="World Wide Corona Virus Cases Deaths",
                  font=dict(family="Courier New, monospace",
                            size=18,
                            color="#7f7f7f")
                 )
fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=0)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()








