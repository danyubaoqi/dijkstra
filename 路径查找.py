import math
import sqlite3
import re
from flask import Flask, render_template, request
from Function import *

# 从数据库提取数据
# 地点信息
allLocation = []
dbCon = sqlite3.connect("db/location.db")
myCursor = dbCon.execute('SELECT location FROM Location')
for i in myCursor:
    allLocation.append(str(i))
myCursor.close()
dbCon.close()
# 换乘信息
change = {}
dbCon = sqlite3.connect("db/change.db")
myCursor = dbCon.execute("SELECT location,nummber FROM change")
for i in myCursor:
    change[i[0]] = i[1]
myCursor.close()
dbCon.close()
# 线路信息
dbCon = sqlite3.connect("db/lineData.db")
myCursor = dbCon.execute("SELECT line,ldata FROM LD")
line = {}
for i in myCursor:
    ldata = re.findall(r"\'.*?\'", i[1])
    line[i[0]] = []
    for j in ldata:
        line[i[0]].append(str(j).replace("'", ""))
myCursor.close()
dbCon.close()
# 两站间距离信息
dbCon = sqlite3.connect("db/路径距离数据.db")
myCursor = dbCon.execute("""SELECT location1,location2,distance FROM LLD""")
dict_distance = {}
for i in myCursor:
    dict_distance[str(change[i[0]]) + "-" + str(change[i[1]])] = i[2]

####
# 前端
####


app = Flask(__name__)


@app.route("/")
def hahahahaha():
    return app.send_static_file("起始查找界面.html")


@app.route("/check/", methods=['post', 'get'])
def check():
    lujing = []
    content = []
    start = request.form["START"]
    end = request.form["END"]
    dijkstra(change[start], change[end],allLocation,lujing,change,dict_distance)

    kaka = make_html(lujing,content,line,)


    return render_template("结果.html", data=kaka)


@app.route("/check/lineData/", methods=['post', 'get'])
def getLineData():
    content2 = ""
    for i in line:
        content2 += str(i) + "   " + str(line[i])
    render_template("查询界面.html", lineData=content2)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
