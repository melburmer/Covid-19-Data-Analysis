# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 13:44:50 2020

@author: Pc
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df = pd.read_csv(r"dataset/covid_19_data.csv")
"""
fig = plt.subplot()
ax = plt.subplot(111)
ax.plot(confirmed['ObservationDate'],confirmed['Confirmed'],label="Confirmed")
ax.plot(recovered['ObservationDate'],recovered['Recovered'],label="Recovered")
ax.plot(deaths['ObservationDate'],deaths['Deaths'],label="Deaths")
plt.xticks(rotation=90)
ax.legend()
plt.show()"""

# çin için benzer line chart çıkaralım

china = df[df["Country/Region"] == "Mainland China"]
confirmed_china = china.groupby('ObservationDate').sum()['Confirmed'].reset_index()
deaths_china = china.groupby('ObservationDate').sum()['Deaths'].reset_index()
recovered_china = china.groupby('ObservationDate').sum()['Recovered'].reset_index()



# usa için benzer line chart çıkaralım

usa = df[df["Country/Region"] == "US"]
confirmed_usa = usa.groupby('ObservationDate').sum()['Confirmed'].reset_index()
deaths_usa = usa.groupby('ObservationDate').sum()['Deaths'].reset_index()
recovered_usa = usa.groupby('ObservationDate').sum()['Recovered'].reset_index()




# italy için benzer line chart çıkaralım

italy = df[df["Country/Region"] == "Italy"]
confirmed_italy = italy.groupby('ObservationDate').sum()['Confirmed'].reset_index()
deaths_italy = italy.groupby('ObservationDate').sum()['Deaths'].reset_index()
recovered_italy = italy.groupby('ObservationDate').sum()['Recovered'].reset_index()



# germany için benzer line chart çıkaralım

germany = df[df["Country/Region"] == "Germany"]
confirmed_germany = germany.groupby('ObservationDate').sum()['Confirmed'].reset_index()
deaths_germany =germany.groupby('ObservationDate').sum()['Deaths'].reset_index()
recovered_germany = germany.groupby('ObservationDate').sum()['Recovered'].reset_index()


plt.rc('ytick', labelsize=20) 
plt.rc('xtick', labelsize=10)
fig, axes = plt.subplots(2,2,sharex=True,figsize=(25,25))

axes[0,0].plot(confirmed_china['ObservationDate'],confirmed_china['Confirmed'],label="Confirmed",color="Blue",linewidth=5)
axes[0,0].plot(recovered_china['ObservationDate'],recovered_china['Recovered'],label="Recovered",color="Green",linewidth=4)
axes[0,0].plot(deaths_china['ObservationDate'],deaths_china['Deaths'],label="Deaths",color="Red",linewidth=4)
axes[0,0].legend(prop={'size': 20},shadow=True)
axes[0,0].set_title("China Corona Virus Cases - Confirmed, Deaths, Recovered",weight="bold",fontsize=20)


axes[0,1].plot(confirmed_usa['ObservationDate'],confirmed_usa['Confirmed'],label="Confirmed",color="Blue",linewidth=5)
axes[0,1].plot(recovered_usa['ObservationDate'],recovered_usa['Recovered'],label="Recovered",color="Green",linewidth=4)
axes[0,1].plot(deaths_usa['ObservationDate'],deaths_usa['Deaths'],label="Deaths",color="Red",linewidth=4)
axes[0,1].legend(prop={'size': 20},shadow=True)
axes[0,1].set_title("USA Corona Virus Cases - Confirmed, Deaths, Recovered",weight="bold",fontsize=20)


axes[1,0].plot(confirmed_italy['ObservationDate'],confirmed_italy['Confirmed'],label="Confirmed",color="Blue",linewidth=5)
axes[1,0].plot(recovered_italy['ObservationDate'],recovered_italy['Recovered'],label="Recovered",color="Green",linewidth=4)
axes[1,0].plot(deaths_italy['ObservationDate'],deaths_italy['Deaths'],label="Deaths",color="Red",linewidth=4)
axes[1,0].legend(loc='upper left', bbox_to_anchor=(0, 1),
           fancybox=True, shadow=True,prop={'size': 20})
axes[1,0].set_title("Italy Corona Virus Cases - Confirmed, Deaths, Recovered",weight="bold",fontsize=20)

axes[1,1].plot(confirmed_germany['ObservationDate'],confirmed_germany['Confirmed'],label="Confirmed",color="Blue",linewidth=5)
axes[1,1].plot(recovered_germany['ObservationDate'],recovered_germany['Recovered'],label="Recovered",color="Green",linewidth=4)
axes[1,1].plot(deaths_germany['ObservationDate'],deaths_germany['Deaths'],label="Deaths",color="Red",linewidth=4)
axes[1,1].legend(loc='upper left', bbox_to_anchor=(0, 1),
           fancybox=True, shadow=True,prop={'size': 20})
axes[1,1].set_title("Germany Corona Virus Cases - Confirmed, Deaths, Recovered",weight="bold",fontsize=20)


axes[1][0].xaxis.set_tick_params(rotation=90)
axes[1][1].xaxis.set_tick_params(rotation=90)

plt.show()







# tüm dünya line chart

confirmed = df.groupby('ObservationDate').sum()['Confirmed'].reset_index()
deaths = df.groupby('ObservationDate').sum()['Deaths'].reset_index()
recovered = df.groupby('ObservationDate').sum()['Recovered'].reset_index()

"""
fig = plt.subplot()
ax = plt.subplot(111)
ax.plot(confirmed['ObservationDate'],confirmed['Confirmed'],label="Confirmed")
ax.plot(recovered['ObservationDate'],recovered['Recovered'],label="Recovered")
ax.plot(deaths['ObservationDate'],deaths['Deaths'],label="Deaths")
plt.xticks(rotation=90)
ax.legend()
plt.show()"""  # bunu da koyabilirim belli değil

confirmed = df.groupby('ObservationDate').sum()['Confirmed'].reset_index()
deaths = df.groupby('ObservationDate').sum()['Deaths'].reset_index()
recovered = df.groupby('ObservationDate').sum()['Recovered'].reset_index()


fig = go.Figure()
fig.add_trace(go.Scatter(x=confirmed['ObservationDate'], 
                         y=confirmed['Confirmed'],
                         mode='lines+markers',
                         name='Confirmed',
                         line=dict(color='blue', width=2)
                        ))
fig.add_trace(go.Scatter(x=deaths['ObservationDate'], 
                         y=deaths['Deaths'],
                         mode='lines+markers',
                         name='Deaths',
                         line=dict(color='Red', width=2)
                        ))
fig.add_trace(go.Scatter(x=recovered['ObservationDate'], 
                         y=recovered['Recovered'],
                         mode='lines+markers',
                         name='Recovered',
                         line=dict(color='Green', width=2)
                        ))
fig.update_layout(
    title='Worldwide Corona Virus Cases - Confirmed, Deaths, Recovered (Line Chart)',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    )
)
fig.show()


############################################### kaggle timelapse 








