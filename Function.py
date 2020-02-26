from math import *
import pymysql
pycon=pymysql.connect("localhost","root","123456","subway",3306)

def get_allLocation():
    cur=pycon.cursor()
    sql="select station_name from station_information"
    cur.execute(sql)
    return cur.fetchall()


def get_change():
    change={}
    cur = pycon.cursor()
    sql = "select station_name,station_id from station_information"
    cur.execute(sql)
    data=cur.fetchall()
    for i in data:
        change[i[0]]=i[1]
    return change

def get_line():

    d={}
    cur=pycon.cursor()
    sql="select * from line_station"
    cur.execute(sql)
    for i in cur.fetchall():
        if i[0] in d:
            d[i[0]].append(i[1])
        else:
            d[i[0]]=[i[1]]

    return d

def get_distance():
    cur=pycon.cursor()
    sql="select * from distance"
    dict_distance = {}
    cur.execute(sql)

    for i in cur.fetchall():
        if i[0] not in dict_distance:
            dict_distance[i[0]]={i[1]:i[2]}
        else:dict_distance[i[0]][i[1]]=i[2]

    return dict_distance

def calPrice(a):
    if a <= 6000:
        return 3
    elif a <= 12000:
        return 4
    elif a <= 22000:
        return 5
    elif a <= 32000:
        return 6
    else:
        return 6 + ceil((a - 32000) / 20000)


#基于迪杰斯特拉计算两站点的最短路径以及换乘
def dijkstra(start, end, allLocation, lujing, change, dict_distance):
    pre_node = []
    visit = []
    distance = []
    n = len(allLocation)

    # 递归查找全程路径
    def printf(p):
        if p != start:
            printf(pre_node[p])
        for i in change:
            if p == change[i]:
                lujing.append(i)

    for j in range(n):
        pre_node.append(False)  # 初始化
        distance.append(999999)
        visit.append(False)
    distance[start] = 0
    for j in range(n):
        best = 99999
        u = 0
        for i in range(n):
            if (not visit[i]) and distance[i] < best:
                best = distance[i]
                u = i
        visit[u] = True
        #如果发现找到终点，结束
        if u == end: break
        Key = dict_distance.keys()
        for v in range(n):
            if u in Key and v in dict_distance[u]:
                if distance[u] + int(dict_distance[u][v]) < distance[v]:
                    distance[v] = distance[u] +dict_distance[u][v]
                    pre_node[v] = u

    if distance[end] < 999999:
        print(str(distance[end]) + "米")
        print(str(calPrice(distance[end])) + "元")
        printf(end)

#判断abc三个站是否是一个路线的，北京地铁不存在不同线路有相邻的两个站
#
def isSameStation(a, b, c, line, content):
    one = []
    two = []
    for i in line:
        if a in line[i]:
            if b in line[i]:  # a,b一条线。b,c一条线
                one.append(i)
                for j in line:
                    if b in line[j]:
                        if c in line[j]:
                            two.append(j)
                            if i == j:
                                return 1
    for i in one:
        if b in line[i]:
            for j in two:
                if c in line[j]:
                    content.append(b)
                    print(b)
                    content.append("在" + b + "换乘" + j + "通往" + c)
                    print("在" + b + "换乘" + j + "通往" + c)

#直接返回html
def make_html(lujing, content, line):
    lenl = len(lujing)
    i = 0
    while i < lenl:
        k = 1
        if i > lenl - 3:
            break
        if k == 1:
            print(lujing[i])
            content.append(lujing[i])
        k = isSameStation(lujing[i], lujing[i + 1], lujing[i + 2], line, content)
        i += 1
        if k != 1:
            i += 1
    while i < lenl:
        content.append(lujing[i])
        i += 1
    content2 = ""
    for i in content:
        content2 += i + "<br>"
    return content2
