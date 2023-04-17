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
from New_New import GDD_new

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
    if type(l1) and type(l2) in [int, np.int32, np.int64, float, np.float32, np.float64] and type(l1) == type(l2):
        m = abs(l1 - l2)
        return m

    else:
        m = ls.ratio(str(l1), str(l2))
        #print(l1,l2,m)
        return 1 - m

def splitdistance(m, n):
    #m = float(m)
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
        cleanlist.sort(key=d.index)
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
        #print(cleanlist)
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
                #print(val,l2)
                if len(l2) != 0:
                    m = GDD_new.iteml(item + '=' + str(val), str(dis), l2, str(dis / len(distancelist)))
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
        nlist_new = []
        for i in range(len(nlist)):
            for j in range(len(nlist[i])):
                nlist_new.append(nlist[i][j])
        return nlist_new
        #return nlist

    else:
        d = df[item].tolist()
        cleanlist = list(set(d))
        cleanlist.sort(key=d.index)
        # print("The Distance of " + str(item) + " is " + str(0))
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
                if len(l2) >= 1:
                    m = GDD_new.iteml(item + '=' + str(val), str(dis), l2, str(dis / len(distancelist)))

                    nxms.append(m)
        # return [nxms]
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
        x = GDD_new.node_s(m[0].replace("(", ''), m[1].replace(")", ""), e[1].rstrip())
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
        slist = []
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
                pairwise = []
                for var in s:
                    if var[1] <= dis:
                        pairwise.append(var[0])
                m = GDD_new.iteml(liter,dis,pairwise,0)
                if len(m.l) > 1:
                    slist.append(m)
                    #print(m)
        if len(slist) > 0:
            samenode.append([slist])
    #print(samenode)


    return samenode

def generkeyword(my_list):
    result_dict = {}
    for item in my_list:
        key = item.atype  # 提取第一个数字作为键
        if key not in result_dict:
            result_dict[key] = []
        result_dict[key].append(item)
    return result_dict

def generatter(my_list):
    result_dict = {}
    for item in my_list:
        key = item.id  # 提取第一个数字作为键
        if key not in result_dict:
            result_dict[key] = []
        result_dict[key].append(item)
    return result_dict

def lablemapping(my_dict,my_list):

    for key, value in my_dict.items():
        if key in my_dict:
            my_dict[key] = my_dict[key] + ([my_list[int(key)]])
        else:
            my_dict.update({key: my_list[int(key)]})
    return my_dict

def creatlist(l1):
    #ddprint(l[0].lists)
    #print(l)
    l = l1
    #print(l)
    d = l[-1]
    s = str(re.sub('[^a-zA-Z]+', '', l[0].name)+'.'+l[0].attribute)
    cleanlist = list(set(d))
    cleanlist.sort(key=d.index)
    #print(s,cleanlist)
    valuelist = []
    for i in range(len(cleanlist)):
        for j in range(len(cleanlist)):
            if j > i:
                val = DDsimilars(cleanlist[i], cleanlist[j])
                valuelist.append(val)
    tt = calculate_delta(valuelist, con)
    distance = abs(tt)
    distancelist = splitdistance(distance, seg)
    l[-1] = distancelist
    #print(l)
    flist = []
    for val in cleanlist:
        #print(val)
        vlist = []
        for j in distancelist:
            result = []
            d_row = len(df[l[0].lists])
            lengthl = len(l) - 1
            #print(d_row,lengthl)
            for i in range(d_row):
                for k in range(lengthl):
                    #print(df[l[k].lists].iloc[i])
                    sm = DDsimilars(val,df[l[k].lists].iloc[i])
                    if sm <= j:
                        #print(i, val, df[l[k].lists].iloc[i], j, sm)
                        result.append(i)
                    else:
                        break
                #result.append(i)
            lst = result
            #print(lst)
            #lst_set = set(lst)
            duplicates = list(set([x for x in lst if lst.count(x) > 1]))
            #print(duplicates,'d')
            #print(val,j,duplicates)
            m = GDD_new.node_s(val,j,duplicates)
            if len(m.attribute) != 0:
                #print(m)
                vlist.append(m)
            #print(vlist)
        if len(vlist) != 0:
            flist.append(vlist)
        #print(val,vlist)

    for x in flist:
        for var1 in x:
            for var2 in x:
                if var1.name != var2.name and var1.attribute == var2.attribute and var1.id == var2.id:
                    x.remove(var2)
    return flist

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
        x = GDD_new.node_s(m[0].replace("(", ''), m[1].replace(")", ""), e[1].rstrip())
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
        slist = []
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
                pairwise = []
                for var in s:
                    if var[1] <= dis:
                        pairwise.append(var[0])
                m = GDD_new.iteml(liter,dis,pairwise,0)
                if len(m.l) >= 1:
                    slist.append(m)
                    #print(m)
        if len(slist) > 0:
            # samenode.append([slist])
            samenode.append(slist)
    #print(samenode,'ssssss')


    return samenode

def combinetitle(title,df):

    titlelist = []
    for liter in title:
        e = liter.split('.')
        m = e[0].split(":")
        x = GDD_new.sattr(m[0].replace("(", ''), m[1].replace(")", ""), e[1].rstrip(),liter,re.sub('[^a-zA-Z]+', '', e[1]))
        titlelist.append(x)
    g = generkeyword(titlelist)
    for item in g:
        k = generatter(g[item])
        g[item] = k
    #keys_list = list(g.keys())
    globe_list = []
    for key, value in g.items():
        #print(key,value)
        ttlist = []
        for key1,value1 in value.items():
            #print(key1,value1)
            tlist = []
            for val in value1:
                #print(val,df[val.lists].tolist())
                tlist.append(df[val.lists].tolist())
            ttlist.append(tlist)
        globe_list.append(ttlist)
    new_graphitem = {}
    nglist = []
    for item in globe_list:
        new_list = []
        for sublist in item:
            new_sublist = []
            for item in sublist:
                new_sublist.extend(item)
            new_list.append(new_sublist)
        nglist.append(new_list)

    for list_item, item in zip(nglist, g):
        for list_i ,item1 in zip(list_item,g[item]):
            g[item][item1] = g[item][item1] + [list_i]
    for t1 in g:
        newdic = {}
        for key,val in g[t1].items():
            s1 = str(re.sub('[^a-zA-Z]+', '', val[0].name)+'.'+val[0].attribute)
            newdic[s1] = val
        g[t1] = newdic
    patternblock = []
    constblock = []
    idblock = []
    for item in g:
        if str(item) != 'id':
            for val in g[item]:
                if len(g[item][val]) > 2:
                    #print(g[item][val])
                    c = creatlist(g[item][val])
                    sb = []
                    for var1 in c:
                        s =  str(re.sub('[^a-zA-Z]+', '', str(g[item][val][0].name))+'.'+ str(g[item][val][0].attribute) + '=' + str(var1[0].id))
                        iteml = GDD_new.iteml(s,var1[0].name,var1[0].attribute,0)
                        if iteml not in sb:
                            sb.append(iteml)
                    patternblock.append(sb)
                elif len(g[item][val]) <= 2:
                    #print(g[item][val])
                    #print(g[item][val],'this is xxx')
                    r = relationbolck(g[item][val][0].lists,seg)
                    #flat_list = [item for sublist in r for item in sublist]
                    #r = flat_list
                    constblock.append(r)
        elif str(item) == 'id':
            for val in g[item]:
                #print(g[item][val])
                r = relationbolck(g[item][val][0].lists, 1)
                #flat_list = [item for sublist in r for item in sublist]
                #r = flat_list
                idblock.append(r)
    vblock = graphrelations(filename,con)
    return patternblock+constblock+idblock+vblock

def mainMethod(lattice, level0Set, dependency_set, literals):
    for i in range(1, len(level0Set)):
        levelSet = []
        print("level ",i)
        start_time = time.time()
        for block1Index, block2Index in combinations([j for j in range(len(lattice[i - 1]))], 2):
            block1 = lattice[i-1][block1Index]
            block2 = lattice[i-1][block2Index]
            prefixSame = True
            if (len(block1.attributeLabels)>1):
                # only the set which the prefixs are same can be combined to generate a new set in the next level
                if (not(operator.eq(block1.attributeLabels[0:len(block1.attributeLabels)-1],block2.attributeLabels[0:len(block2.attributeLabels)-1]))):
                    prefixSame = False
            if (len(block1.literalsSet)!=0 and len(block2.literalsSet)!=0 and prefixSame):
                literalsSet = []
                attributeLabels = []
                combineFirstOrder = 1
                if block1.attributeLabels[len(block1.attributeLabels)-1] < block2.attributeLabels[len(block2.attributeLabels)-1]:
                    attributeLabels = copy.deepcopy(block1.attributeLabels)
                    attributeLabels.append(block2.attributeLabels[len(block2.attributeLabels)-1])
                else:
                    combineFirstOrder = 2
                    attributeLabels = copy.deepcopy(block2.attributeLabels)
                    attributeLabels.append(block1.attributeLabels[len(block1.attributeLabels)-1])
                prefixHashMap = dict()
                for literals1 in block1.literalsSet:
                    # literals1 = [literals1]
                    keyStr = ''
                    for k in range(len(literals1) - 1):
                        keyStr += str(literals1[k].name + ' ' + str(literals1[k].sigma))
                    if (keyStr in prefixHashMap.keys()):
                        prefixHashMap[keyStr].append(literals1[len(literals1) - 1])
                    else:
                        prefixHashMap[keyStr] = [literals1[len(literals1) - 1]]
                for literals2 in block2.literalsSet:
                    # literals2 = [literals2]
                    keyStr = ''
                    for k in range(len(literals2) - 1):
                        keyStr += str(literals2[k].name + ' ' + str(literals2[k].sigma))
                    if (keyStr in prefixHashMap.keys()):
                        if (combineFirstOrder == 1):
                            for literal in prefixHashMap[keyStr]:
                                literalSet = literals2[0:len(literals2) - 1]
                                literalSet.append(literal)
                                literalSet.append(literals2[len(literals2) - 1])
                                matches = literalSet[0].l
                                for literal in literalSet:
                                    matches = tuple(set(matches).intersection(set(literal.l)))
                                if len(matches) > 0:
                                    literalsSet.append(literalSet)
                        else:
                            for literal in prefixHashMap[keyStr]:
                                literalSet = copy.deepcopy(literals2)
                                literalSet.append(literal)
                                matches = literalSet[0].l
                                for literal in literalSet:
                                    matches = tuple(set(matches).intersection(set(literal.l)))
                                if len(matches) > 0:
                                    literalsSet.append(literalSet)
                if (len(literalsSet) > 0):
                    levelSet.append(GDD_new.Block(attributeLabels, literalsSet))
                    print("one_block_literals_number", len(literalsSet))
        print("levelSet", len(levelSet))
        end_time = time.time()
        print('one_level_combination_time_cost', end_time - start_time, "s")
        start_time = time.time()
        lattice.append(levelSet)
        compute_dependencies_and_prune(lattice[i - 1], lattice[i], dependency_set)
        end_time = time.time()
        print('one_level_compute_dependencies_time_cost', end_time - start_time, "s")
        lattice[i - 1] = []
    print("literals number", literals)
    print("attribute number", attriNumber)

def compute_dependencies_and_prune(levelSet1,levelSet2,dependency_set):
    for block1 in levelSet1:
        attributeLabels_1 = block1.attributeLabels
        for block2 in levelSet2:
            attributeLabels_2 = block2.attributeLabels
            if (set(attributeLabels_1).issubset(set(attributeLabels_2))):
                rhsIndex = -1000
                for i in range(len(attributeLabels_2)):
                    if attributeLabels_2[i] not in attributeLabels_1:
                        rhsIndex = i
                        break
                # print(attributeLabels_1,attributeLabels_2,rhsIndex)
                prefixHashMap = dict()
                reLiteralsSet = []
                for literals2 in block2.literalsSet:
                    keyStr = ''
                    for k in range(len(literals2)):
                        if k != rhsIndex:
                            keyStr += str(literals2[k].name + ' ' + str(literals2[k].sigma))
                    if (keyStr in prefixHashMap.keys()):
                        prefixHashMap[keyStr].append([literals2, literals2[rhsIndex]])
                    else:
                        prefixHashMap[keyStr] = [[literals2, literals2[rhsIndex]]]
                for literals1 in block1.literalsSet:
                    # literals1 = [literals1]
                    lhsSet = literals1
                    lhsMatches = lhsSet[0].l
                    for literal in lhsSet:
                        lhsMatches = tuple(set(lhsMatches).intersection(set(literal.l)))
                    keyStr = ''
                    for k in range(len(literals1)):
                        keyStr += str(literals1[k].name + ' ' + str(literals1[k].sigma))
                    if (keyStr in prefixHashMap.keys()):
                        for value in prefixHashMap[keyStr]:
                            rhs = value[1]
                            rhsMatches = rhs.l
                            if (set(lhsMatches).issubset(set(rhsMatches))):
                                # isUseful = False
                                # tmp = rhs.variable
                                # for literal in lhsSet:
                                #     if tmp!=literal.variable or tmp=="None" or literal.variable=="None":
                                #         # more than one entity in dependency
                                #         isUseful = True
                                #         break
                                # if isUseful:
                                dependency = ""
                                for i in range(len(lhsSet)):
                                    if (i == len(lhsSet) - 1):
                                        dependency += lhsSet[i].name + ' ' + str(lhsSet[i].sigma)
                                    else:
                                        dependency += lhsSet[i].name + ' ' + str(lhsSet[i].sigma) + ";;"
                                dependency += "->"
                                dependency += rhs.name + ' ' + str(rhs.sigma)
                                # print(dependency)
                                dependency_set.append(dependency)
                                reLiteralsSet.append(value[0])
                for reliterals in reLiteralsSet:
                    # prune
                    block2.literalsSet.remove(reliterals)

def clean_redundant(dependency_set, fileout):
    # for dependency in dependency_set:
    #     print(dependency)
    dependency_set_fu = copy.deepcopy(dependency_set)  # Remove redundancy on the left
    for dependency1 in dependency_set:
        s = dependency1.split('->')
        s1 = s[0]
        s2 = s[-1]
        for dependency2 in dependency_set:
            if dependency2 != dependency1:
                w = dependency2.split('->')
                w1 = w[0]
                w2 = w[-1]
                if w2 == s2:
                    left = s1.replace(';;', ' ').split(' ')
                    right = w1.replace(';;', ' ').split(' ')
                    if len(left) == len(right) and left[::2] == right[::2]:
                        for i in range(len(left)):
                            if i % 2 == 1 and float(left[i]) < float(right[i]) and dependency1 in dependency_set_fu:
                                dependency_set_fu.remove(dependency1)
                                break
    res_dict = {}
    rel_dict = {}
    for dependency in dependency_set_fu:
        s = dependency.split('->')
        s1 = s[0]
        s2 = s[-1]
        if s1 in rel_dict.keys():
            tem = rel_dict[s1]
            tem.append(s2)
            rel_dict[s1] = tem.copy()
            res_dict[s1] = tem.copy()
        else:
            lists = [s2]
            rel_dict[s1] = lists.copy()
            res_dict[s1] = lists.copy()

    for key, value in rel_dict.items():    # Remove redundancy on the right side
        valid_value = copy.deepcopy(value)
        for i in range(len(value)):
            for j in range(len(value)):
                ary = value[i].split(' ')
                aryy = value[j].split(' ')
                if ary[0] != aryy[0] or i == j:
                    continue
                if float(aryy[1]) > float(ary[1]) and value[j] in valid_value:
                    valid_value.remove(value[j])
        rel_dict[key] = copy.deepcopy(valid_value)
        res_dict[key] = copy.deepcopy(valid_value)

    # for key1, value1 in rel_dict.items():
    #     for key2, value2 in rel_dict.items():
    #         left = key1.replace(';;', ' ').split(' ')
    #         right = key2.replace(';;', ' ').split(' ')
    #         if len(left) == len(right) and left[::2] == right[::2]:
    #             for i in range(len(left)):
    #                 for j in range(len(value1)):
    #                     if i % 2 == 1 and float(left[i]) < float(right[i]):
    #                         if key1 in res_dict.keys():

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
                    if sli[1 - i] in new_value1 or sli[i - 1] in new_value2:
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
            fileout.write(key + '->' + rhs + "\n")
            vaildNumber += 1

    print(";;before: dependency number " + str(len(dependency_set)))
    print(";;after: dependency number " + str(vaildNumber))
    fileout.write(";;before: dependency number " + str(len(dependency_set)) + "\n")
    fileout.write(";;after: dependency number " + str(vaildNumber) + "\n")

if __name__ == "__main__":
    #g = glob.glob('*.txt')
    #for gi in g:
        filename = 'produce_Table2.txt'
        files = filename + 'result2.txt'
        file = pd.read_csv(filename, delimiter=";;", engine='python')
        fileout = open(files, 'w', encoding='utf-8')
        df = pd.DataFrame(file)
        title = []
        for cloum_name in df.columns:
            title.append(df[cloum_name].name)
        con = 1
        start_time = time.time()
        thresord = int(con * len(df))
        candite = []  # contains the every attribute with it items
        pure_list = ['id']
        relation_candait = []
        seg = 3
        blocks = combinetitle(title,df)
        # for i in blocks:
        #     print(i)
        candite = blocks
        literals = 0
        for i in range(len(candite)):
            literals += len(candite[i])
            for j in range(len(candite[i])):
                candite[i][j] = [candite[i][j]]
        for k in candite:
            print(k)
        level0Set = []
        attriNumber = len(candite)
        L = []
        lattice = []
        for i in range(attriNumber):
            L.append((i,))
        literalsSet = []
        for i in range(len(candite)):
            # print(literalsSet)
            level0Set.append(GDD_new.Block([i], candite[i]))
        lattice.append(level0Set)
        dependency_set = []
        mainMethod(lattice, level0Set, dependency_set, literals)
        clean_redundant(dependency_set, fileout)
        end_time = time.time()
        print("start_time:", start_time)
        print("end_time:", end_time)
        print("time cost:", end_time - start_time, "s")
        fileout.write(";;time cost: " + str(end_time - start_time) + " s")
        fileout.close()
