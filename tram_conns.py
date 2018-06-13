# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 21:48:10 2018

@author: ASUS
"""

import pandas as pd
from lxml import html
import urllib
from bs4 import BeautifulSoup

# Getting links for tramways
base_url = "http://bkv-jaratok.altalanos.info/jarmu.php?type=0"
file = urllib.request.urlopen(base_url)
data = file.read()
soup = BeautifulSoup(data,"html.parser") 
ul = soup.findAll('ul')[1]

columns = ['main','connect']
tram_conns = pd.DataFrame(columns=columns)
index = 0

for li in ul.contents:
    url = "http://bkv-jaratok.altalanos.info" + li.contents[0]['href']
    main = li.contents[0].getText().split(" ")[0]
    if "A" not in main:
        file = urllib.request.urlopen(url)
        data = file.read()
        soup = BeautifulSoup(data,"html.parser") 
        ul = soup.findAll('ul')[3]
        for li in ul.contents:
            connect = li.getText().split(" ")[0]
            if "A" not in connect:
                line_df = pd.DataFrame([[main,connect]], columns=columns, index = [index])
                index += 1
                tram_conns = tram_conns.append(line_df)

tram_conns.to_csv("tram_conns.csv",encoding='utf-8', index=False)