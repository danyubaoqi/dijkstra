# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from urllib import request
import sqlite3

# 爬取北京地铁官网信息
lineCompile = re.compile(r">.*?线")
dataFromWeb = request.urlopen("http://www.bjsubway.com/station/zjgls/").read().decode("gb2312")
# 使用beautifulsoup解析
oBS = BeautifulSoup(dataFromWeb, "html.parser")
# 按照table获取各个线的信息
dataLine = oBS.find_all("table", width=True)
lineAll = (re.findall(">(.*?线)", str(dataLine)))
delTr = re.compile(r"<tr.*?>.*?|<td .*?>.*?</td>")
delAll = re.compile("\n|上行|下行|<.*?>|/")
oBS = oBS.find_all("tr")  #
oBS = oBS[2:]  #
allStation = []
lineData={}
for i in oBS:
    i = str(i)
    i = delAll.sub("", i)
    if i.find("方向") == -1 and i.find("相邻") == -1:
        allStation.append(i)

for i in allStation:
    print(i)
findDistance = re.compile(r"\d{3,6}")
dictDistance = {}
allLocation = []

for i in allStation:
    distance = findDistance.findall(i)  # j
    k = i.split(distance[0])
    k = k[0].split("――")
    allLocation.append(k[0])
    allLocation.append(k[1])
    dictDistance[k[0] + "――" + k[1]] = int(distance[0])  # 转化为字典
    dictDistance[k[1] + "――" + k[0]] = int(distance[0])

allLocation = {}.fromkeys(allLocation).keys()

# diDian = sqlite3.connect("""db/location.db""")
# try:
#     diDian.execute("""CREATE TABLE Location(location)""")
# except:
#     1
# for i in allLocation:
#     diDian.execute("""INSERT INTO Location
#     (location)
#     VALUES( """ + '"' + str(i) + '"' + ')')
#     diDian.commit()
# diDian.close()
####################
# 统计各个站在哪条线
#################
# lineData = sqlite3.connect("lineData.db")
# try:
#     lineData.execute("CREATE TABLE LD(line,ldata)")
# except:
#     pass
# line = {}
# for i in lineAll:
#     line[i] = []
# for i in allLocation:
#     for j in dataLine:
#         j = str(j)
#         if i in j:
#             for k in lineAll:
#                 if k in j:
#                     line[k].append(i)
# for i in line:
#     lineData.execute("""INSERT INTO LD
#     (line,ldata)
#     VALUES (""" + '"' + str(i) + '","' + str(line[i]) + '")')
#     lineData.commit()
# lineData.close()
# # 给每个站赋值
# ChangeCoon = sqlite3.connect("change.db")
# try:
#     ChangeCoon.execute("""CREATE TABLE change(location,nummber)""")
# except:
#     1
# change = {}
# j = 0
# for i in allLocation:
#     change[i] = j
#     ChangeCoon.execute("""INSERT INTO change
#     (location,nummber)
#     VALUES (""" + '"' + str(i) + '",' + str(j) + ')')
#     ChangeCoon.commit()
#     j += 1
# ChangeCoon.close()
#
# # 变成双向
# dbCoon = sqlite3.connect("路径距离数据.db")
# try:
#     dbCoon.execute("""CREATE TABLE LLD(location1,location2,distance)""")
# except:
#     1
# dictJuli2 = {}
# for i in dictDistance:
#     j = i.split("――")
#     dictJuli2[str(change[j[0]]) + "-" + str(change[j[1]])] = dictDistance[i]
#     dbCoon.execute("""insert into LLD
#     (location1,location2,distance)
#     VALUES (""" + '"' + j[0] + '","' + j[1] + '",' + str(dictDistance[i]) + ")")
#     dbCoon.commit()
# dbCoon.close()
