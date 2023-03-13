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
        #print(item,d)
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
        #nxms = []
        nlist = []
        #for dis in distancelist:
        for val in cleanlist:
            l1 = []
            #for val in cleanlist:
            for dis in distancelist:
                l2 = []
                for i in range(len(d)):
                    if DDsimilars(val, d[i]) <= dis:
                        l2.append(i)
                #l1.append(l2)
                #print(l1)
                if len(l2) != 1:
                    m = GDD.iteml(item + '=' + str(val), str(dis), l2, str(dis / len(distancelist)))
                    #print(m)
                    l1.append(m)
                    #nxms.append(m)
            if len(l1) != 0:
                nlist.append(l1)
        #print(nlist)
        for nxms in nlist:
            for var1 in nxms:
                for var2 in nxms:
                    if var1.name == var2.name and var1.sigma != var2.sigma and var1.l == var2.l:
                        nxms.remove(var2)
                if len(var1.l) == 0:
                    nxms.remove(var1)
            #l = len(nxms)
            #if l > 1:
                #print(nxms)
            #r_block_filter(nxms,cleanlist)
        #print(nlist)
        return nlist
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
        return [nxms]

def splitliters(liter):
    e = liter.split('.')
    m = e[0].split(":")
    l1 = m[0].replace("(", '')
    l2 = m[1].replace(")", "")
    l3 = e[1].rstrip()
    l4 = re.sub('[^a-zA-Z]+', '', l2)
    return [l1,l2,l3,l4]

def combineset(complementaryset,templist):
    Lable = {}

    attrlist = []
    names = []
    outlist = []
    complementaryset2 = complementaryset.copy()
    for i in range(len(complementaryset)):
        entitylist = []
        for j in range(len(complementaryset)):
            if j > i:
                if splitliters(complementaryset[i])[0] == splitliters(complementaryset[j])[0] and splitliters(complementaryset[i])[2] == splitliters(complementaryset[j])[2]:
                        entitylist.append(complementaryset[i])
                        entitylist.append(complementaryset[j])
        names.append(entitylist)
    #attrlist.append(names)
    print(names)

    #return 0


def graphrelations(filename,con,title):
    ntitle = title.copy()
    file = pd.read_csv(filename, delimiter=";;", engine='python')

    temp = []
    for n in title:
        e = n.split('.')
        m = e[0].split(":")
        x = GDD.node_s(m[0].replace("(", ''), m[1].replace(")", ""), e[1].rstrip(),n)

        temp.append(x)
    for liter1 in temp:
        for liter2 in temp:
            if liter1.id ==liter2.id and liter1.attribute == liter2.attribute and liter1 != liter2:
                if liter1.sname in title:
                    title.remove(liter1.sname)
    complementaryset = list(set(ntitle) - (set(title)))
    #print(re.sub('[^a-zA-Z]+', '', temp[0].name))
    print(list(set(complementaryset)))
    comb = combineset(complementaryset,temp)







if __name__ == "__main__":
    #g = glob.glob('*.txt')
    #for gi in g:
        filename = 'produce_Table4.txt'
        files = filename + 'result40.txt'
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
        '''for item in title:
            if 'id' not in item:
                # print("How many different distances do you want about", title[i])
                # seg = int(input())
                seg = 3
                x = relationbolck(item,seg)
                relation_candait.append(x)
            elif 'id' in item:
                seg = 1
                x = relationbolck(item,seg)
                relation_candait.append(x)'''
        #print(relation_candait)
        #s = r_block_filter(relation_candait)
        vblocks = graphrelations(filename,con,title)
        #print(vblocks)
