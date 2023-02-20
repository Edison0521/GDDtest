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
        print("The best delta of " + str(item) + " is " + str(abs(tt)))
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
        print("The Distance of " + str(item) + " is " + str(0))
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
        print(relation_candait)

