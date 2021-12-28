# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 09:27:29 2021

@author: lgabor
"""

import pandas as pd
import urllib
from bs4 import BeautifulSoup


def collect_schedule(date):
    columns = ['ID','line','station','direction','lat','long']
    stations = pd.DataFrame(columns=columns)
    index = 0
    
    tram_urls = pd.read_csv("line_urls.csv")
    
    for i in range(len(tram_urls)):
        line =  tram_urls.iat[i,0]
        for k in range(2):
            url = tram_urls.iat[i,1].replace("ok/","/") + "/" + str(k)
        
            file = urllib.request.urlopen(url)
            data = file.read()
            soup = BeautifulSoup(data,"html.parser")
            line = soup.findAll("title")[0].getText().split(" megállók, útvonal, menetrend - ")[0].split("-")[0].replace("Fogaskerekű (","")
            direction = soup.findAll("title")[0].getText().split(" megállók, útvonal, menetrend - ")[1].split(" irány")[0].strip().replace('"','')
            div = soup.findAll('div')
            for j in div:
                if j.has_attr('id'):
                    if "stop_" in j['id']:
                        id = j['id'].replace("stop_","")
                        soup = BeautifulSoup(str(j),"html.parser")
                        a = soup.findAll("a")
                        station = soup.findAll("strong")[0].getText().split(" megálló")[0].replace('"','')
                        lat,long = a[2]['href'].replace("javascript:showStreetView(","").replace(")","").split(",")[:2]
                        # print(id, line, station, direction, lat,long)
                        line_df = pd.DataFrame([[id, line, station, direction, lat,long]], columns=columns, index = [index])
                        index += 1
                        stations = stations.append(line_df)
    stations.to_csv("tram_stations.csv",encoding='utf-8', index=False, quoting=False)
    
    tram_stations = list(stations['ID'])
    
    columns = ['ID','line','station','direction','lat','long','time']
    schedule = pd.DataFrame(columns=columns)
    index = 0

    for i in tram_stations:
        print(i)
        try:
            url = "https://bkv-jaratok.altalanos.info/megallo-menetrend/" + i
            file = urllib.request.urlopen(url)
            data = file.read()
            soup = BeautifulSoup(data,"html.parser")
            station = soup.findAll("title")[0].getText().split(" megálló")[0].strip().replace('"',"")
        
            divs = soup.findAll("div", {"class": "panel panel-info route-times date_" + date + " hidden"})
            
            for div in divs:
                soup = BeautifulSoup(str(div),"html.parser")
                h3 = soup.findAll("h3")
                if "villamos" in h3[0].getText():
                    soup = BeautifulSoup(str(h3[0]),"html.parser")
                    lat, lon = str(soup.findAll("a")[1]['href']).split("=")[-1].split(",")
                    line = h3[0].getText().split(" villamos")[0].replace("-as","").replace("-es","").replace("-os","")
                    if "❆" not in line and "A" not in line and "B" not in line and "M" not in line:
                        direction = h3[0].getText().split("irány |")[0].split("villamos ")[1].strip().replace('"',"")
                        soup = BeautifulSoup(str(div),"html.parser")
                        times = soup.findAll("div", {"class": "panel-body"})
                        times = str(times[0].getText().encode('ascii', 'ignore').decode("utf-8")).replace("  ",",").replace(",,","").replace("\n","").replace("\r","")[:-1]
                        times = times.split(",")
                        for time in times:
                            print(url.split("/")[-1], line, direction, station, lat, lon, time)
                            line_df = pd.DataFrame([[url.split("/")[-1], line, direction, station, lat, lon, time]], columns=columns, index = [index])
                            index += 1
                            schedule = schedule.append(line_df)
        except:
            pass
    print(schedule)
    schedule.to_csv("schedule.csv",encoding='utf-8', index=False)

date = "20220115"
collect_schedule(date)
