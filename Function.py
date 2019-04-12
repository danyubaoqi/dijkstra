from math import *


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
        if u == end: break
        Key = dict_distance.keys()
        for v in range(n):
            if (str(u) + "-" + str(v)) in Key:
                if distance[u] + int(dict_distance[str(u) + "-" + str(v)]) < distance[v]:
                    distance[v] = distance[u] + int(dict_distance[str(u) + "-" + str(v)])
                    pre_node[v] = u

    if distance[end] < 999999:
        print(str(distance[end]) + "米")
        print(str(calPrice(distance[end])) + "元")
        printf(end)


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
