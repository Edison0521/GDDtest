import numpy as np
import pandas as pd
import time
import itertools
import Levenshtein as ls
import re
from string import digits


class Blocks(object):
    def __init__(self, Namelist, name, distance,tuples):
        self.Namelist = Namelist
        self.name = name
        self.distance = distance
        self.tuples = tuples

    def __repr__(self):
        return "%s %s %s %s" % (self.Namelist, self.name, self.distance, self.tuples)

class node_s(object):
    def __init__(self, id, name, attribute):
        self.id = id
        self.name = name
        self.attribute = attribute

    def __repr__(self):
        return "%s %s %s" % (self.id, self.name, self.attribute)


class snode(object):
    def __init__(self, name, attribute):
        self.name = name
        self.attribute = attribute

    def __repr__(self):
        return "%s %s" % (self.name, self.attribute)


class Dtems(object):
    def __init__(self, itemname, newname, items):
        self.name = itemname
        self.newname = newname
        self.sigma = items

    def __repr__(self):
        return "%s %s %s" % (self.name, self.sigma, self.newname)


class DD(object):

    def __init__(self, rhs: str, lhs: str, items):
        self.rhs = rhs
        self.lhs = lhs
        self.items = items

    def __repr__(self):
        return "%s %s %s" % (self.lhs, self.rhs, self.items)


class LCP(object):
    def __init__(self, level_name: str, items: list, cand: list):
        self.name = level_name
        self.items = items
        self.cand = cand

    def __repr__(self):
        return "%s %s %s " % (self.name, self.items, self.cand)


class iteml(object):
    def __init__(self, itemname: str, sigma, l, shares):
        self.name = itemname
        self.sigma = sigma
        self.l = l
        self.shares = shares

    def __repr__(self):
        return "%s %s %s %s" % (self.name, self.sigma, self.l, self.shares)


def getPrelist(k):
    x = str(k)
    '''
    u = re.sub(r'[0-9]+', '', u)
    u = u.replace('(','')
    t = u.replace(":",".")
    x = t.replace("=","=")
    e = x.split('.')
    '''
    # x = u.replace("=","=")
    e = x.split('=')
    # print(e)
    return e[0]


def getAttrbutes(filename: str):
    """

    :param filename:the csv name
    :return: the Attribute list
    """
    attrs = pd.read_csv(filename, header=None)
    sx = []
    df = pd.DataFrame(attrs)
    for i in range(0, len(df.loc[0])):
        sx.append(df.loc[0][i])
    return sx


def Union_set(listA, listB):
    # Intersection
    retC = list(set(listA).intersection(set(listB)))
    return retC


def difference_set(listA, listB):
    # difference between A & B
    retE = list(set(listB).difference(set(listA)))
    return retE


def get_sub_set(nums):
    '''

    :param nums:the list of all single attribute
    :return: Complete Collection
    '''
    sub_sets = [[]]
    for x in nums:
        sub_sets.extend([item + [x] for item in sub_sets])
    return sub_sets


def itertools_chain(a):
    l = list(itertools.chain.from_iterable(a))
    return l


def spilt(l: list):
    l = list(itertools.combinations(l, 2))
    # l = itertools_chain(l)
    return l


def My_duplicate(l1):
    # duplicate removal
    t = l1[:]
    for i in l1:
        while t.count(i) > 1:
            del t[t.index(i)]
    # order
    t.sort(key=l1.index)
    return t


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


def DDsimilars(l1, l2):
    '''

    :param l1:the first item to be compair
    :param l2: the second one
    :return: the Similarity
    '''
    # print(type(l1))
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


def maxculsters(s, distance):
    maxmalobjects = []
    # print(s)
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
    #print(s[x[0][0]][1], 'o')
    return x, s[x[0][0]][1]


oi = []


def createtunple(name, tmpl, confidence, thresord, segment):
    '''

    :param file: filename
    :param clomname: the Attributes
    :param confidence: confidence
    :return:the list of tuple
    '''
    l2 = tmpl.tolist()
    # print(type(l2[0]))
    lt = l2.copy()
    for i in range(len(l2)):
        if pd.isna(l2[i]) == True:
            lt.remove(l2[i])
    l2 = lt
    if len(l2) > 0:
        '''
        This section is a comparison of the character variable gap
        Not yet completed
        '''
        '''
               This section is a comparison of the character variable gap
               Not yet completed
               '''
        # print(l2)
        l1 = []
        for i in range(len(l2)):
            l1.append(i)

        # print(l1)
        l3 = dict(zip(l1, l2))  # key is mainkey value is tuple id
        l4 = dict(zip(l3.values(), l3.keys()))
        # print(l3.items())
        s = sorted(l3.items(), key=lambda x: x[1])
        # print(s)
        valuelist = list(l4.keys())
        predeltalist = []
        for i in range(len(valuelist)):
            for j in range(len(valuelist)):
                if j > i:
                    predeltalist.append(DDsimilars(valuelist[i], valuelist[j]))
        # print(predeltalist)
        tt = calculate_delta(predeltalist, confidence)
        print("The best delta of " + str(name) + " is " + str(abs(tt)))
        distance = abs(tt)
        # q = Items(name,distance)
        xmxs = []
        distancelist = splitdistance(distance, segment)
        for i in range(len(distancelist)):
            utmp = maxculsters(s, distancelist[i])
            if utmp[0] != []:
                # m = iteml(name, distancelist[i], utmp)
                m = iteml(name+'='+str(utmp[1]), distancelist[i], utmp[0], (i + 1) / len(distancelist))
                xmxs.append(m)
        # print(xmxs)
        return xmxs
    else:
        return []


def judegename(u):
    u1 = []
    u1.append(u)
    u = u1
    for i in range(len(u)):
        # t = u[i].replace(":", ".")
        e = u[i].split('.')
        m = e[0].split(":")
        x = Dtems(m[0].replace("(", ''), m[1].replace(")", ""), e[1])
        # print(x)


def combinelist(filename):
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
        x = node_s(m[0].replace("(", ''), m[1].replace(")", ""), e[1])
        temp.append(x)
    list1 = []
    liters = []
    for i in range(len(temp)):
        lt = []
        if int(temp[i].name.join(filter(str.isdigit, temp[i].name))) > 0:

            s1 = str("(" + temp[i].id + ":" + temp[i].name + ")" + '.' + temp[i].attribute + "=")
            l1 = str("(" + temp[i].id + ":" + temp[i].name + ")" + '.' + temp[i].attribute)
            for q in range(0, i):
                s2 = str("(" + temp[q].id + ":" + temp[q].name + ")" + '.' + temp[q].attribute)
                l2 = str("(" + temp[q].id + ":" + temp[q].name + ")" + '.' + temp[q].attribute)
                if temp[i].attribute == temp[q].attribute and re.sub('[^a-zA-Z]+', '', temp[q].name) == re.sub(
                        '[^a-zA-Z]+', '', temp[i].name):
                    s = s1 + s2
                    lt.append(l1)
                    lt.append(l2)

                    list1.append(s)
                    liters.append(lt)
    # print(liters)
    samenode = []
    for i in range(len(list1)):
        samenode.append(snode(list1[i], liters[i]))
    return samenode


def compute_dependencies(L, R):
    '''
    Procedure COMPUTE_DEPENDENCIES described in [1]
    '''
    #for i in range(len(L)):



if __name__ == "__main__":
    filename = 'produce_Table0.txt'
    files = "xFGDD1.txt"
    file = pd.read_csv(filename, delimiter=";;", engine='python')
    df = pd.DataFrame(file)
    # title = getAttrbutes(filename)
    title = []
    for cloum_name in df.columns:
        title.append(df[cloum_name].name)
        # print(df[cloum_name].name)
    print("please input the confidence:")
    # con = float(input())
    con = 1
    starttime = time.time()
    print("The confidence is", con)
    print("please input the Thresord")
    # thresord = 10
    thresord = int(con * len(df))
    print("The thresord is", thresord)
    candite = []  # contains the every attribute with it items
    prelist = ['id']

    for i in range(len(title)):
        # temp = []
        u = title[i]
        # print(type(u[i]))
        t = u.replace(":", ".")
        e = u.split('.')
        # print(e)
        if e[1] not in prelist and title[i] not in prelist:
            # if e[1] != 'id':
            # print(title[i])
            print("How many different distances do you want about", title[i])
            # seg = int(input())
            seg = 1
            # if title[i] != "id":
            ut = createtunple(title[i], df[title[i]], con, thresord, seg)
            for i in range(len(ut)):
                for j in range(len(ut[i].l)):
                    ut[i].l[j] = spilt(ut[i].l[j])
                ut[i].l = list(set(itertools_chain(ut[i].l)))
            candite.append(ut)
        comb = combinelist(filename)
    comblist = []
    '''
    for i in range(len(candite)):
        ugg = []
        for j in range(len(candite)):
            if candite[i] != [] and j > i and candite[j] != []:
                for k in range(len(comb)):
                    if candite[i][0].name and candite[j][0].name in comb[k].attribute:
                        # if candite[i][0].sigma == candite[j][0].sigma:
                        for m in range(len(candite[i])):
                            us = Union_set(candite[i][m].l, candite[j][m].l)
                            #uc = iteml(comb[k].name, candite[i][m].sigma, us)
                            uc = iteml(comb[k].name,candite[i][m].sigma,us,str(''))
                            #print(uc)
                            ugg.append(uc)
                            #candite.append(ugg)
    '''
    Cendthime = time.time()
    totalL = Cendthime - starttime
    print('Candit has created', totalL)
    rhsnameset = []
    rhslistset = []
    tmp = []
    for i in range(len(candite)):
        if len(candite[i]) > 0:
            u = candite[i][len(candite[i]) - 1].name + "=" + str(candite[i][len(candite[i]) - 1].sigma)
            t = candite[i][len(candite[i]) - 1].l
            rhsnameset.append(u)
            rhslistset.append(t)
            tmp.append(candite[i][len(candite[i]) - 1].name)
        else:
            break
    '''
    p1 = list(filter(None, get_sub_set(rhsnameset)))
    p2 = list(filter(None, get_sub_set(rhslistset)))

    p3 = list(filter(None, get_sub_set(tmp)))

    lcp = []  # the RHS set
    for i in range(len(p1)):
        lcp.append(LCP(p1[i], p2[i], p3[i]))

    tlcp = lcp.copy()
    for i in range(len(lcp)):
        if len(lcp[i].name) >= 2:
            t = Union_set(lcp[i].items[0], lcp[i].items[1])
            lcp[i].items = t
        else:
            if lcp[i].items[0] != []:
                lcp[i].items = lcp[i].items[0]
            tlcp.remove(lcp[i])
        if lcp[i].items == [] and len(lcp[i].items) < thresord:
            tlcp.remove(lcp[i])

    Rhsendthime = time.time()
    totalR = Rhsendthime - Cendthime
    print('Rhs has created', totalR)
    # print(tlcp)
    origindd = []
    # t = []
    for i in range(len(tlcp)):
        for j in range(len(candite)):
            for k in range(len(candite[j])):
                if candite[j][k].name not in tlcp[i].cand:
                    # print(candite[j][0].name,tlcp[i].cand)
                    e = difference_set(candite[j][0].l, tlcp[i].items)
                    #print(e,'jjj')
                    if e != []:
                        if "=" not in candite[j][0].name:
                        #origindd.append(DD(candite[j][0].name + '=' + str(candite[j][0].sigma), tlcp[i].name))
                            origindd.append(DD(candite[j][0].name+'='+str(candite[j][0].shares) , tlcp[i].name , str(',tunple is '+str(e))))
                        else:
                            origindd.append(DD(candite[j][0].name, tlcp[i].name , str(',tunple is '+str(e))))
                        break
    endtime = time.time()
    attrlist = []

    f = open(files, 'w+')
    for i in range(len(origindd)):
        u = str(origindd[i].rhs)
            # u = re.sub(r'[0-9]+', '', u)
            # u = u.replace('(','')
            # t = u.replace(":",".")
        x = u.replace("=", "=")
        e = x.split('=')
            # print(e)
        if e[0] not in attrlist:
            attrlist.append(e[0])
            # print(origindd[i].lhs)
        for j in range(len(origindd[i].lhs)):
            m = origindd[i].lhs[j]
            e = getPrelist(m)
            if e not in attrlist:
                attrlist.append(e)

            # print(e[2])
        if "id" not in origindd[i].lhs and origindd[i].rhs:
            k = 0
            print(origindd[i], file=f)

    print(endtime - starttime)

    print(attrlist)
    '''
    print(len(candite))
    L0 = candite
    RHS = candite
    print("caerat Level 0")
    compute_dependencies(L0,L0)
    print(L0)
    for i in range(len(L0)):
        for j in range(len(L0)):
            if j > i:
                for k in range(len(L0[i])):
                    x = 0
