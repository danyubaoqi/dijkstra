# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from urllib import request as wohaoshuai
import sqlite3

lineCompile = re.compile(r">.*?线")
dataFromWeb = wohaoshuai.urlopen("http://www.bjsubway.com/station/zjgls/").read().decode("gb2312")
oBS = BeautifulSoup(dataFromWeb, "html.parser")
dataLine = oBS.find_all("table", width=True)
lineAll2 = (re.findall(">.*?线", str(dataLine)))
lineall = []
for i in lineAll2:
    i = i.strip(">")
    lineall.append(i)
delTr = re.compile(r"<tr.*?>.*?|<td .*?>.*?</td>")
delAll = re.compile("\n|上行|下行|<.*?>|/")
oBS = oBS.find_all("tr")  #
oBS = oBS[2:]  #
All = []
for i in oBS:
    i = str(i)
    i = delAll.sub("", i)
    if i.find("方向") == -1 and i.find("相邻") == -1:
        All.append(i)
for i in All:
    print(i)
find1 = re.compile(r"\d{3,6}")
dictJuli = {}
for i in All:
    juli = find1.findall(i)  # j
    k = i.split(juli[0])
    k = k[0].split("――")
    dictJuli[k[0] + "――" + k[1]] = int(juli[0])  # 转化为字典
    dictJuli[k[1] + "――" + k[0]] = int(juli[0])
allDidian = []
for i in dictJuli:
    i = i.split("――")
    for j in i:
        allDidian.append(j)
allDidian = {}.fromkeys(allDidian).keys()
diDian = sqlite3.connect("""location.db""")
try:
    diDian.execute("""CREATE TABLE Location(location)""")
except:
    1
for i in allDidian:
    diDian.execute("""INSERT INTO Location
    (location)
    VALUES( """ + '"' + str(i) + '"' + ')')
    diDian.commit()
diDian.close()
####################
# 统计各个站在哪条线
#################
lineData = sqlite3.connect("lineData.db")
try:
    lineData.execute("CREATE TABLE LD(line,ldata)")
except:
    1
line = {}
for i in lineall:
    line[i] = []
for i in allDidian:
    for j in dataLine:
        j = str(j)
        if i in j:
            for k in lineall:
                if k in j:
                    line[k].append(i)
for i in line:
    lineData.execute("""INSERT INTO LD
    (line,ldata)
    VALUES (""" + '"' + str(i) + '","' + str(line[i]) + '")')
    lineData.commit()
lineData.close()
# 给每个站赋值
ChangeCoon = sqlite3.connect("change.db")
try:
    ChangeCoon.execute("""CREATE TABLE change(location,nummber)""")
except:
    1
change = {}
j = 0
for i in allDidian:
    change[i] = j
    ChangeCoon.execute("""INSERT INTO change
    (location,nummber)
    VALUES (""" + '"' + str(i) + '",' + str(j) + ')')
    ChangeCoon.commit()
    j += 1
ChangeCoon.close()

# 变成双向
dbCoon = sqlite3.connect("路径距离数据.db")
try:
    dbCoon.execute("""CREATE TABLE LLD(location1,location2,distance)""")
except:
    1
dictJuli2 = {}
for i in dictJuli:
    j = i.split("――")
    dictJuli2[str(change[j[0]]) + "-" + str(change[j[1]])] = dictJuli[i]
    dbCoon.execute("""insert into LLD
    (location1,location2,distance)
    VALUES (""" + '"' + j[0] + '","' + j[1] + '",' + str(dictJuli[i]) + ")")
    dbCoon.commit()
dbCoon.close()
