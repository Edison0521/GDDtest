
import numpy as np
import pandas as pd
import time
import itertools
import Levenshtein as ls
import re
from itertools import combinations
import operator
import glob
import copy

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

class Block:
    '''
    the strcture of one block of each lattice level
    '''

    def __init__(self, attributeLabels, literalsSet):
        self.attributeLabels = attributeLabels
        self.literalsSet = literalsSet

    def __repr__(self):
        return str(self.attributeLabels)


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


def sub_set(listA, listB):
    # difference between A & B
    retE = list(set(listB).difference(set(listA)))
    return retE

def difference_set(listA, listB):
    # difference between A & B
    retE = list(set(listB)^(set(listA)))
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
    #print(t)
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
    #print(l1,type(l1))
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


def  maxculsters(s, distance):
    maxmalobjects = []
    #print(s)
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
    origint = tmpl.tolist()
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
        #print(s)
        valuelist = list(l4.keys())
        predeltalist = []
        for i in range(len(valuelist)):
            for j in range(len(valuelist)):
                if j > i:
                    predeltalist.append(DDsimilars(valuelist[i], valuelist[j]))
        # print(predeltalist)
        tt = calculate_delta(predeltalist, confidence)
        #print("The best delta of " + str(name) + " is " + str(abs(tt)))
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
        #print(valuelist)
        #print(origint)
        #print(distancelist)
        '''for liter in valuelist:
            t2 = []
            for i in range(len(origint)):
                t1 = []
                for distances in distancelist:
                    d = DDsimilars(liter,origint[i])
                    if d <= distances:
                        print(name,liter,i,distances)
                        t1.append(i)
                #t1.sort()
                t2.append(t1)
            print(t2)'''
        nxms = []
        for dis in distancelist:
            l1 = []
            for val in valuelist:
                #print(val)
                l2 = []
                for i in range(len(origint)):
                    if DDsimilars(val,origint[i]) <= dis:
                        l2.append(i)
                l1.append(l2)
                if len(l2) != 1:
                #print('this is',l2,dis,name,val)
                #print('this is', name , '=' , val , 'distance = ' , dis , 'tunple = ' , l2)
                    m = iteml(name+'='+str(val),str(dis),[l2],str(dis/len(distancelist)))
                    nxms.append(m)
        #print(nxms,'n')
        #print(xmxs,'o')
        return nxms
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
        x = node_s(m[0].replace("(", ''), m[1].replace(")", ""), e[1].rstrip())
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
            #print(liter)
            #print(df[liter[0]],df[liter[1]])
            distanceset = []
            for k in range(len(df)):
                for p in range(len(df)):
                    #print(df[liter[0]][k],df[liter[1]][p])

                    u = DDsimilars(str(df[liter[0]][k]),str(df[liter[1]][p]))
                    distanceset.append(u)
            #print(distanceset)
            tt = calculate_delta(distanceset,con)
            #print(tt)
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
            #print(tuplelist)
            m = iteml(liter[0]+' and '+liter[1], abs(tt), tuplelist, None)
            sameliters.append(m)
    for i in range(len(list1)):
        samenode.append(snode(list1[i], liters[i]))
    cosameliters = sameliters.copy()
    for liter in sameliters:
        if len(liter.l) == 0:
            cosameliters.remove(liter)
    return cosameliters


def purns(l1,l2):
    #print(prunlist)
    u = l1
    t = get_sub_set(l2)
    FFlag = True
    FLag = False
    for liter in t:
        if len(liter) != 0:
            tliter = liter
            tliter.append(u)
            #print(tliter,'m')
            if tliter not in prunlist:
                #print(tliter)
                m = 0
                FFlag = True
                break
                #return True
            else:
                FFlag = False
                #return False
                #print('x')
                #print(l1,l2,prunlist)
        
    #print(l2,prunlist)

    return FFlag

def clean_redundant(dependency_set,fileout):
    res_dict = {}
    rel_dict = {}
    for dependency in dependency_set:
        s = dependency.split('->')
        s1 = s[0]
        #print(s1)
        # s1 = s1.replace('{', '')
        # s1 = s1.replace('}', '')
        s2 = s[-1]
        # s2 = s2.replace("\n", '')
        if s1 in rel_dict.keys():
            tem = rel_dict[s1]
            tem.append(s2)
            rel_dict[s1] = tem.copy()
            res_dict[s1] = tem.copy()
        else:
            lists = [s2]
            rel_dict[s1] = lists.copy()
            res_dict[s1] = lists.copy()
    
    vaildNumber = 0
    for item in rel_dict.items():
        key = item[0]
        value = item[1]
        sli = key.split(';;')
        validSet = value.copy()
        for single_value in value:
            if len(sli) == 2:
                # A,B->C, A,C->B
                for i in range(0, 2):
                    new_str1 = sli[i] + ';;' + single_value
                    new_str2 = single_value + ';;' + sli[i]
                    new_value1 = []
                    new_value2 = []
                    if new_str1 in res_dict.keys():
                        new_value1 = res_dict[new_str1]
                    if new_str2 in res_dict.keys():
                        new_value2 = res_dict[new_str2]
                    if sli[1 - i] in new_value1 or sli[i-1] in new_value2:
                        if single_value in validSet:
                            validSet.remove(single_value)
            # A->[B,C],B->[C]
            if single_value in rel_dict.keys():
                two_lev = res_dict[single_value]
                for three_lev in two_lev:
                    if three_lev in value:
                        if three_lev in validSet:
                            validSet.remove(three_lev)
            
        res_dict[key] = validSet.copy()
        
        for rhs in validSet:
            fileout.write("{"+key+'} -> '+rhs+"\n")
            vaildNumber += 1

    #fileout.write("\n"+information[0]+"\n")
    fileout.write("before: dependency number "+str(len(dependency_set))+"\n")
    fileout.write("after: dependency number "+str(vaildNumber)+"\n")


def crlattice(levelset,dependency0_set,lavel0set):
    #print(levelset)
    levelsets = []
    for i in range(len(lavel0set)):
        #print(lavel0set[i])
        for k in range(len(levelset)):
            #print(lavel0set[i],levelset[k])
            if i not in levelset[k][0]:
                #if levelset[k][0] not in prunlist:
                    #print(i,levelset[k][0])
                    J_Flag = False
                    for j in reversed(levelset[k][1]) :
                        if len(j.l) != 0 and len(candite[i]) != 0:
                            if J_Flag == True:
                                    break
                            #print(j.l,'s',candite[i][0])
                            e = difference_set(j.l,candite[i][0].l)
                            #if len(e) != 0 and len(e) < 5:
                            if (len(sub_set(j.l,candite[i][0].l)) == 0 and len(sub_set(candite[i][0].l,j.l))) != 0:
                                #print(j)
                                newlevelset = list(levelset[k][0])
                                newlevelset.append(i)
                                newitem = iteml(j.name+ ' ' +str(j.sigma)+','+candite[i][0].name+ ' ' +str(candite[i][0].sigma),None,Union_set(candite[i][0].l,j.l),None)
                                #print(newitem)
                                #print(newlevelset)
                                Newlevetliter = (newlevelset,[newitem])
                                levelsets.append(Newlevetliter)

                                J_Flag = True
                            elif len(e) == 0:
                            #else:
                                preprunelist = copy.deepcopy(levelset[k][0])
                                preprunelist.append(i)
                                preprunelist.sort()
                                dependency = ""
                                #lhsSet1 = levelset[k][0]

                                dependency += j.name + ' ' + str(j.sigma)

                                dependency += "->"
                                dependency += candite[i][0].name + ' ' + str(candite[i][0].sigma)
                                dependency_set.append(dependency)
                                prunlist.append(preprunelist)

    #for depen in dependency_set:
        #m = 0
        #print(depen)
    #print(preprunelist)
    return levelsets

def execl(l,r):
    #print(r)
    if l != []:
        if len(l[0][0]) == 0:
            return
        elif len(l[0][0]) != 0:
            #print(len(l[0][0]))
            #print(Rhsste)
            #print(r)
            l = crlattice(l,depedency,r)
        #print(l)
        #execl(l)
            return execl(l,r)



if __name__ == "__main__":
    #g = glob.glob('*.txt')
    #for gi in g:
        filename = 'produce_Table0.txt'
        files = filename + 'result.txt'
        file = pd.read_csv(filename, delimiter=";;", engine='python')

        f2 = open(files + 'noredunt.txt','w',encoding='utf-8')
        file = pd.read_csv(filename, delimiter=";;", engine='python')
        df = pd.DataFrame(file)
        # title = getAttrbutes(filename)
        title = []
        for cloum_name in df.columns:
            title.append(df[cloum_name].name)
            # print(df[cloum_name].name)
        #print("please input the confidence:")
        # con = float(input())
        con = 1
        starttime = time.time()
        #print("The confidence is", con)
        #print("please input the Thresord")
        # thresord = 10
        thresord = int(con * len(df))
        #print("The thresord is", thresord)
        candite = []  # contains the every attribute with it items
        prelist = []

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
                #print("How many different distances do you want about", title[i])
                # seg = int(input())
                seg = 3
                # if title[i] != "id":
                ut = createtunple(title[i], df[title[i]], con, thresord, seg)
                for i in range(len(ut)):
                    for j in range(len(ut[i].l)):
                        ut[i].l[j] = spilt(ut[i].l[j])
                    ut[i].l = list(set(itertools_chain(ut[i].l)))
                candite.append(ut)
        comb = combinelist(filename,con)
        Cendthime = time.time()
        totalL = Cendthime - starttime
        #print('Candit has created', totalL)
        rhsnameset = []
        rhslistset = []
        L0 = candite
        RHS = candite
        level = 0
        lattice = []
        level0Set = []
        for i in range(len(comb)):
            #print(comb[i])
            candite.append([comb[i]])
        attriNumber = len(candite)
        L = []
        for i in range(attriNumber):
            L.append((i,))
        literalsSet = []
        for i in range(len(candite)):
            #print(literalsSet)
            level0Set.append(Block([i], [candite[i]]))
        lattice.append(level0Set)
        #print(lattice)
        dependency_set = []
        outlist = []
        L0 = candite
        RHS = candite

        level = 1
        lattice = []
        level0Set = []
        depedency = []
        prunlist = []
        #candite.sort()
        '''for cad in candite:
            print(cad)'''
        #print(candite[16])
        attriNumber = len(candite)
        L = {}
        for i in range(len(candite)):
            n1 = i
            n2 = candite[i]
            L[n1] = n2
        #lattice.append(level0Set)
        for i in range(len(L)):
            lattice.append(([i],L[i]))
        RHSset = candite
        #print(len(L))
        #print(len(lattice))
        #print('level 1')
        execl(lattice,RHSset)
        f = open(files, 'w+')
        for depen in dependency_set:
            m = 0
            print(depen,file=f)
        #f2 = open('noredunt.txt','w',encoding='utf-8')
        clean_redundant(dependency_set,f2)
        endtime = time.time()
        totaltime = endtime -  - starttime
        #print('totaltime is',totaltime)

    