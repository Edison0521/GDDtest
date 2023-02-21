import numpy as np
import pandas as pd
import time
import itertools
import Levenshtein as ls
import re
import copy
from itertools import combinations
import operator
import glob
from GDDMining import GDD

def diff(l1: list):
    '''
    Determining whether a subset exists in a set
    :param l1: a list
    :return: a list whitout subset
    '''
    l1 = [x for x in l1 if x]
    temp = l1.copy()
    for i in range(len(l1)):
        for j in range(len(l1)):
            if j > i:
                if set(l1[j]).issubset(set(l1[i])):
                    if l1[j] in temp:
                        temp.remove(l1[j])
    return temp


def maxculsters(s, distance):
    maxmalobjects = []
    #print(s,distance)
    for i in range(len(s)):
        maxcluster = []
        for j in range(len(s)):
            if j > i:
                pr = i
                pl = j
                judge = DDsimilars(s[pl][1], s[pr][1])
                # print(s[pl], s[pr],judge,distance)
                if judge <= distance:
                    if s[pr][0] not in maxcluster:
                        maxcluster.append(s[pr][0])
                    maxcluster.append(s[pl][0])
        # print(maxcluster)
        if len(maxcluster) != 0:
            # print(s[maxcluster[len(maxcluster) - 1]][1],s[maxcluster[0]][1],'p')
            # if s[maxcluster[len(maxcluster) - 1]][1] != s[maxcluster[0]][1]:
            maxmalobjects.append(maxcluster)
    # print(maxmalobjects)
    x = diff(maxmalobjects)
    if x != []:
        return x, s[x[0][0]][1]
    else:
        return x,None

def calculate_delta(arr, confidence):
    '''

    :param arr: A list made up of numbers
    :param confidence:confidence
    :return:bestdelta
    '''
    n = len(arr)
    if n > 0:
        removals = n - round(n * confidence)

        best_delta = arr[-1] - arr[0]
    else:
        return 0

    # removing outliers in such a way that minimize delta:
    for i in range(removals + 1):
        best_delta = min(best_delta, arr[-(removals - i + 1)] - arr[i])
    if best_delta % 1 == 0:
        return best_delta
    else:
        return round(best_delta, 2)


def DDsimilars(l1, l2):
    '''

    :param l1:the first item to be compair
    :param l2: the second one
    :return: the Similarity
    '''
    # print(l1,type(l1))
    if type(l1) and type(l2) in [int, np.int32, np.int64, float, np.float32, np.float64]:
        m = abs(l1 - l2)
        return m

    else:
        m = ls.ratio(l1, l2)
        return 1 - m


def splitdistance(m, n):
    if m % 1 == 0:
        # n = int(n)
        assert n > 0
        quotient = int(m / n)
        remainder = m % n
        if remainder > 0:
            x = [quotient] * (n - remainder) + [quotient + 1] * remainder
            b = []
            for i in range(1, len(x) + 1):
                c = sum(x[:i])
                b.append(c)
            b = sorted(set(b), key=b.index)
            return b
        if remainder < 0:
            x = [quotient - 1] * -remainder + [quotient] * (n + remainder)
            b = []
            for i in range(1, len(x) + 1):
                c = sum(x[:i])
                b.append(c)
            return b
        x = [quotient] * n
        b = []
        for i in range(1, len(x) + 1):
            c = sum(x[:i])
            b.append(c)
        b = sorted(set(b), key=b.index)
        return b
    else:
        assert n > 0
        quotient = m / n
        x = [quotient] * n
        b = []
        for i in range(1, len(x) + 1):
            c = sum(x[:i])
            b.append(round(c, 2))
        b = sorted(set(b), key=b.index)
        return b


def relationbolck(item,seg):
    if 'id' not in item:
        d = df[item].tolist()
        cleanlist = list(set(d))
        valuelist = []
        for i in range(len(cleanlist)):
            for j in range(len(cleanlist)):
                if j > i :
                    val = DDsimilars(cleanlist[i],cleanlist[j])
                    valuelist.append(val)
        tt = calculate_delta(valuelist, con)
        #print("The best delta of " + str(item) + " is " + str(abs(tt)))
        #print(tt,'2')
        distance = abs(tt)
        distancelist = splitdistance(distance, seg)
        nxms = []
        for dis in distancelist:
            l1 = []
            for val in cleanlist:
                l2 = []
                for i in range(len(d)):
                    if DDsimilars(val, d[i]) <= dis:
                        l2.append(i)
                l1.append(l2)
                if len(l2) != 1:
                    m = GDD.iteml(item + '=' + str(val), str(dis), l2, str(dis / len(distancelist)))
                    nxms.append(m)
        for var1 in nxms:
            for var2 in nxms:
                if var1.name == var2.name and var1.sigma != var2.sigma and var1.l == var2.l:
                    nxms.remove(var2)
        return nxms
    else:
        d = df[item].tolist()
        cleanlist = list(set(d))
        #print("The Distance of " + str(item) + " is " + str(0))
        distance = 0
        distancelist = splitdistance(distance, seg)
        nxms = []
        for dis in distancelist:
            l1 = []
            for val in cleanlist:
                l2 = []
                for i in range(len(d)):
                    if val == d[i]:
                        l2.append(i)
                l1.append(l2)
                if len(l2) > 1:
                    m = GDD.iteml(item + '=' + str(val), str(dis), l2, str(dis / len(distancelist)))
                    nxms.append(m)
        return nxms

def graphrelations(filename,con):
    filename = filename
    with open(filename, 'r', encoding='utf-8') as f:  # 打开⽂件
        lines = f.readlines()  # 读取所有⾏
    u = lines[0].split(";;")
    # print(u)
    temp = []
    for i in range(len(u)):
        # print(type(u[i]))
        t = u[i].replace(":", ".")
        e = u[i].split('.')
        m = e[0].split(":")
        x = GDD.node_s(m[0].replace("(", ''), m[1].replace(")", ""), e[1].rstrip())
        #print(x)
        temp.append(x)
    list1 = []
    liters = []
    for i in range(len(temp)):
        lt = []
        if int(temp[i].name.join(filter(str.isdigit, temp[i].name))) > 0:
            s1 = str("(" + temp[i].id + ":" + temp[i].name + ")" + '.' + temp[i].attribute + "=")
            #print(s1)
            l1 = str("(" + temp[i].id + ":" + temp[i].name + ")" + '.' + temp[i].attribute)
            for q in range(0, i):
                s2 = str("(" + temp[q].id + ":" + temp[q].name + ")" + '.' + temp[q].attribute)
                l2 = str("(" + temp[q].id + ":" + temp[q].name + ")" + '.' + temp[q].attribute)
                #print(temp[i].attribute,temp[q].attribute)
                if temp[i].attribute == temp[q].attribute and re.sub('[^a-zA-Z]+', '', temp[q].name) == re.sub(
                        '[^a-zA-Z]+', '', temp[i].name):
                    s = s1 + s2
                    #print(s)
                    lt.append(l1)
                    lt.append(l2)

                    list1.append(s)
                    liters.append(lt)
    #print(list1)
    file = pd.read_csv(filename, delimiter=";;", engine='python')
    df = pd.DataFrame(file)
    samenode = []
    for liter in list1:
        if 'id' not in liter:
            l = liter.split('=')
            #print(l)
            d1 = df[l[0]]
            d2 = df[l[1]]
            #print(len(d1))
            distacne_l = []
            for i in range(len(d1)):
                #print(DDsimilars(d1.iloc[i],d2.iloc[i]))
                #print(d1.iloc[i],d2.iloc[i])
                dist = DDsimilars(d1.iloc[i],d2.iloc[i])
                distacne_l.append(abs(dist))
            #print(calculate_delta(distacne_l,con))
            tt = abs(calculate_delta(distacne_l,con))
            dis_l = splitdistance(tt,seg)
            #print(dis_l)
            l2 = distacne_l
            l1 = []
            for i in range(len(l2)):
                l1.append(i)
            l3 = dict(zip(l1, l2))  # key is mainkey value is tuple id
            s = sorted(l3.items(), key=lambda x: x[1])
            #print(s)
            for dis in dis_l:
                '''utmp = maxculsters(s,dis)
                if utmp[0] != []:
                    # m = iteml(name, distancelist[i], utmp)
                    m = GDD.iteml(liter , dis, utmp[0], (dis + 1) / 1)
                    #print(m)
                    samenode.append(m)'''
                #x = 0
                pairwise = []
                for var in s:
                    #print(var)
                    if var[1] <= dis:
                        #print(var[0])
                        pairwise.append(var[0])
                m = GDD.iteml(liter,dis,pairwise,0)
                #print(m)
                if len(m.l) > 1:
                    samenode.append(m)
    return samenode

def r_block_filter(rblocks):
    #print(rblocks)
    for blo in rblocks:
        '''for var1,var2 in blo:
            if var1.name == var2 and var1.dis != var2.dis:
                print(var1,var2)'''
        if len(blo) > 1:
            for var1 in blo:
                print(var1)

if __name__ == "__main__":
    #g = glob.glob('*.txt')
    #for gi in g:
        filename = 'produce_Table0.txt'
        files = filename + 'result0.txt'
        file = pd.read_csv(filename, delimiter=";;", engine='python')
        df = pd.DataFrame(file)
        title = []
        for cloum_name in df.columns:
            title.append(df[cloum_name].name)
        con = 1
        starttime = time.time()
        thresord = int(con * len(df))
        candite = []  # contains the every attribute with it items
        pure_list = ['id']
        #print(title)
        relation_candait = []
        for item in title:
            if 'id' not in item:
                # print("How many different distances do you want about", title[i])
                # seg = int(input())
                seg = 3
                x = relationbolck(item,seg)
                relation_candait.append(x)
            elif 'id' in item:
                seg = 1
                x = relationbolck(item,seg)
                relation_candait.append(x)
        #print(relation_candait)
        s = r_block_filter(relation_candait)
        vblocks = graphrelations(filename,con)
        #print(vblocks)

