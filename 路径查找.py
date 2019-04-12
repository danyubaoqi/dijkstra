import math
import sqlite3
import re
from flask import Flask, render_template, request
from Function import *

# 从数据库提取数据
# 地点信息
allLocation = get_allLocation()

# 换乘信息
change = get_change()

# 线路信息
line = get_line()
# 两站间距离信息
dict_distance = get_distance(change)
####
# 前端
####


app = Flask(__name__)


@app.route("/")
def hahahahaha():
    return app.send_static_file("index.html")


@app.route("/check/", methods=['post', 'get'])
def check():
    lujing = []
    content = []
    start = request.form["START"]
    end = request.form["END"]
    dijkstra(change[start], change[end], allLocation, lujing, change, dict_distance)

    data = make_html(lujing, content, line)

    return render_template("结果.html", data=data)


@app.route("/lineData/")
def getLineData():
    print(line)
    return render_template("查询界面.html", line=line)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
