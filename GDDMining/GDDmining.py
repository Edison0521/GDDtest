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
                if len(l2) != 1:
                    m = GDD.iteml(item + '=' + str(val), str(dis), l2, str(dis / len(distancelist)))
                    nxms.append(m)
        return nxms
def combinelist(filename,con):
    sameliters = []
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
    ##print(temp[5].attribute,temp[10].attribute)
    #print(len(temp[10].attribute.rstrip()))
    #print(DDsimilars(temp[10].attribute,'Year'))
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
    # print(liters)
    file = pd.read_csv(filename, delimiter=";;", engine='python')
    df = pd.DataFrame(file)
    #print(len(df))
    #print(df[liters[0][0]])
    samenode = []
    for liter in liters:
        u = liter[0]
        t = u.replace(":", ".")
        e = u.split('.')
        #print(e)
        if 'id' not in e:
            distanceset = []
            for k in range(len(df)):
                for p in range(len(df)):
                    u = DDsimilars(str(df[liter[0]][k]),str(df[liter[1]][p]))
                    distanceset.append(u)
            tt = calculate_delta(distanceset,con)
            print("The best delta of " + str(liter[0]+liter[1]) + " is " + str(abs(tt)))
            pretuplelist = []
            tuplelist = []
            for x in range(len(df)):
                #print(df[liter[0]][x],df[liter[1]][x],DDsimilars(df[liter[0]][x],df[liter[1]][x]),abs(tt))
                if DDsimilars(df[liter[0]][x],df[liter[1]][x]) <= abs(tt):
                    pretuplelist.append(x)
            if len(pretuplelist) > 1:
                for i in range(len(pretuplelist)):
                    for j in range(len(pretuplelist)):
                        if j > i:
                            tuplelist.append((i,j))
            m = GDD.iteml(liter[0]+' and '+liter[1], abs(tt), tuplelist, None)
            sameliters.append(m)
    for i in range(len(list1)):
        samenode.append(GDD.snode(list1[i], liters[i]))
    cosameliters = sameliters.copy()
    for liter in sameliters:
        if len(liter.l) == 0:
            cosameliters.remove(liter)
    print(cosameliters)
    return cosameliters


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
        combinelist(filename,con)

