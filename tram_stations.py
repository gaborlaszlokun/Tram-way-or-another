# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 19:47:00 2018

@author: ASUS
"""

import pandas as pd
import numpy as np
from lxml import html
import urllib
from bs4 import BeautifulSoup


columns = ['line','station']
tram_stations = pd.DataFrame(columns=columns)
index = 0

base_url = "https://bkv-jaratok.altalanos.info/jarat.php?r=3"
tram_conns = pd.read_csv("tram_conns.csv")
lines = tram_conns.main.unique()

for line in lines:
    url = base_url + str(line[:2]).zfill(2)
    if "M" in line:
        url += "4&d=0"
    else:
        url += "0&d=0"
    #print(url)
    file = urllib.request.urlopen(url)
    data = file.read()
    soup = BeautifulSoup(data,"html.parser")
    ul = soup.findAll('ul',{"class":"list-unstyled"})[0]
    soup = BeautifulSoup(str(ul),"html.parser")
    span = soup.findAll('span')
    for st in span:
        station = st.getText()
        line_df = pd.DataFrame([[line,station]], columns=columns, index = [index])
        index += 1
        tram_stations = tram_stations.append(line_df)

tram_stations.to_csv("tram_stations.csv", index=False)


table = pd.pivot_table(tram_stations,index="station", columns="line",aggfunc=len, fill_value=0)
piv_df = pd.DataFrame(table)


col_list= list(piv_df)
piv_df["sum"]  = piv_df[col_list].sum(axis=1)

print(piv_df)
piv_df.to_csv("stations_and_lines.csv")
