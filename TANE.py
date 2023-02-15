from pandas import *
from collections import defaultdict#字典类
import numpy as NP
import sys
# import pdb
# pdb.set_trace()


def findCplus(x): # this computes the Cplus of x as an intersection of smaller Cplus sets
    global dictCplus
    thesets=[]
    for a in x:
        #计算的过程涉及到了递归调用
        if x.replace(a,'') in dictCplus.keys():
            temp = dictCplus[x.replace(a,'')]
        else:
            temp=findCplus(x.replace(a,'')) # compute C+(X\{A}) for each A at a time
        #dictCplus[x.replace(a,'')] = temp
        thesets.insert(0, set(temp))
    if list(set.intersection(*thesets)) == []:
        cplus = []
    else:
        cplus = list(set.intersection(*thesets))  # compute the intersection in line 2 of pseudocode
    return cplus

def check_superkey(x):
    global dictpartitions#关于每个属性集的剥离分区
    if ((dictpartitions[x] == [[]]) or (dictpartitions[x] == [])):#如果剥离分区为空，则说明π_x只有单例等价类组成
        return True
    else:
        return False


def computeE(x):#属性集为x
    global totaltuples#元组数
    global dictpartitions#关于每个属性集的剥离分区
    doublenorm = 0
    for i in dictpartitions[''.join(sorted(x))]:#''.join(sorted(x))先将x排序--即BCA to ABC，再转换为字符串，用''隔开
        #测试 print(i) # i为剥离分区中的等价类，对于testABCD-test，x=D,i取[0,3]、[1,2]
        doublenorm = doublenorm + len(i)#doublenorm存储所有等价类的大小的和
    e = (doublenorm-len(dictpartitions[''.join(sorted(x))]))/float(totaltuples)
    return e

#测试 testdataABCD.csv
print(computeE('A'))#4-2 / 4 = 0.5
print(computeE('C'))#0-0/4 = 0
print(dictpartitions)


def validfd(y,z):#验证Y->是否符合函数依赖
    if y=='' or z=='': return False
    ey = computeE(y)#计算误差e(X)
    eyz = computeE(y+z)#计算误差e(XU{A})
    if ey == eyz :#引理3.5
        return True
    else:
        return False

def computeCplus(x):
    # this computes the Cplus from the first definition in section 3.2.2 of TANE paper.
    #output should be a list of single attributes
    global listofcolumns#始终=[A,B,C,D]
    listofcols = listofcolumns[:]#copy
    if x=='': return listofcols # because C+{phi} = R(φ=Phi)
    cplus = []
    for a in listofcols:#A∈R并且满足如下条件：
        for b in x:
            temp = x.replace(a,'')
            temp = temp.replace(b,'')
            if not validfd(temp, b):
                cplus.append(a)
    return cplus

def compute_dependencies(level, listofcols):  # 参数为Li层，即当前层的属性？还是直接A,B,C,D
    global dictCplus  # 属性-右方集dict
    global finallistofFDs  # FD List
    global listofcolumns  # 属性集List
    # FUN1:计算所有X∈Li的右方集Cplus
    # 通过上层结点{A})计算当前层的每个X的Cplus(X)
    # 或通过computeCplus
    print(listofcols)
    for x in level:
        thesets = []
        for a in x:
            if x.replace(a, '') in dictCplus.keys():  # 如果Cplus(X\A)已经在当前右方集List中
                temp = dictCplus[x.replace(a, '')]  # temp存入的是Cplus(X\A)---即X\A的右集合
            else:  # 否则，计算右方集
                temp = computeCplus(x.replace(a, ''))  # compute C+(X\{A}) for each A at a time
                dictCplus[x.replace(a, '')] = temp  # 存入dictCplus中
            thesets.insert(0, set(temp))  # 通过set，将temp转换为集合，再将该对象插入到列表的第0个位置
        if list(set.intersection(*thesets)) == []:  # set.intersection(set1, set2 ... etc)求并集
            dictCplus[x] = []
        else:
            dictCplus[x] = list(set.intersection(*thesets))  # 即伪代码第二行中的计算交集
    # FUN2：找到最小函数依赖
    # 并对Cplus进行剪枝(最小性剪枝)：1.删掉已经成立的2.取掉必不可能的 留下的仍然是“有希望的”'''
    for x in level:

        for a in x:
            if a in dictCplus[x]:  # 即如果A取得X与Cplus的交集
                # if x=='BCJ': print "dictCplus['BCJ'] = ", dictCplus[x]
                if validfd(x.replace(a, ''), a):  # 即X\{A}->A函数依赖成立
                    finallistofFDs.append([x.replace(a, ''), a])  # line 6
                    print("compute_dependencies:level：%s adding key FD: %s" % (level, [x.replace(a, ''), a]))
                    dictCplus[x].remove(a)  # line 7
                    listofcols = listofcolumns[:]  # copy listofcolumns 实则为接下来剪枝做准备
                    for j in x:  # this loop computes R\X
                        if j in listofcols: listofcols.remove(j)  # 此时listofcools更新

                    for b in listofcols:  # 在 C+(X)删掉所有属于R\X即不属于X的元素，即所留下的Cpuls元素全部属于X
                        #                         print(b)
                        #                         print (dictCplus[x])
                        if b in dictCplus[x]:
                            #                             print(b)
                            #                             print (dictCplus[x])
                            dictCplus[x].remove(b)
    for x in level:
        print(x)
        print(dictCplus[x])

def prune(level):
    global dictCplus#属性集的右方集
    global finallistofFDs#FD
    for x in level: # line 1
        '''Angle1:右方集修剪'''
        if dictCplus[x]==[]: # line 2
            level.remove(x) # line 3：若Cplus(X)=φ,则删除X
        '''Angle2:键修剪'''
        if check_superkey(x): # line 4   ### should this check for a key, instead of super key??? Not sure.
            temp = dictCplus[x][:]# 初始化temp 为 computes cplus(x)
            #1. 求得C+(X) \ X
            for i in x: # this loop computes C+(X) \ X
                if i in temp: temp.remove(i)# temp为C+(X) \ X
            #2. line 5：for each a ∈ Cplus(X)\X do
            for a in temp:
                thesets=[]
                #3. 计算Cplus((X+A)\ {B})
                for b in x:
                    if not( ''.join(sorted((x+a).replace(b,''))) in dictCplus.keys()):
                    # ''.join(sorted((x+a).replace(b,''))表示的就是XU{a}\{b}
                        dictCplus[''.join(sorted((x+a).replace(b,'')))] = findCplus(''.join(sorted((x+a).replace(b,''))))
                    thesets.insert(0,set(dictCplus[''.join(sorted((x+a).replace(b,'')))]))
                #4. 计算Cplus((X+A)\ {B})交集，判断a是否在其中
                if a in list(set.intersection(*thesets)): # line 6 set.intersection(*thesets)为求所有thesets元素的并集
                    finallistofFDs.append([x, a]) # line 7
                    #测试
                    print ("pruning:level：%s adding key FD: %s"%(level,[x,a]))
            # 只要x是超键，就要剪掉x。
            if x in level:level.remove(x)#如果此时在line3中已经删除X,则不执行.
def generate_next_level(level):
    #首先令 L[i+1] 这一层为空集
    nextlevel=[]
    for i in range(0,len(level)): # 选择一个属性集
        for j in range(i+1, len(level)): # 将其与后面的所有属性集进行比较
            #如果这两个元素属于同一个前缀块，那么就可以合并:只有最后一个属性不同，其余都相同
            if ((not level[i]==level[j]) and level[i][0:-1]==level[j][0:-1]):  # i.e. line 2 and 3
                x = level[i]+level[j][-1]  #line 4  X = Y U Z
                flag = True
                for a in x: # this entire for loop is for the 'for all' check in line 5
                    if not(x.replace(a, '') in level):
                        flag=False
                if flag==True:
                    nextlevel.append(x)
                    #计算新的属性集X上的剥离分区
                    #=pi_y*pi_z（其中y为level[i]，z为level[j]）
                    stripped_product(x, level[i] , level[j] ) # compute partition of x as pi_y * pi_z (where y is level[i] and z is level[j])
    return nextlevel

def stripped_product(x,y,z):
    global dictpartitions#剥离分区
    global tableT
    tableS = ['']*len(tableT)
    #partitionY、partitionZ是属性集Y、Z上的剥离分区，已知！
    #partitionY is a list of lists, each list is an equivalence class
    partitionY = dictpartitions[''.join(sorted(y))]
    partitionZ = dictpartitions[''.join(sorted(z))]
    print("y:%s partitionY:%s,z:%s partitionZ%s"%(y,partitionY,z,partitionZ))
    partitionofx = [] # line 1
    for i in range(len(partitionY)): # line 2
        for t in partitionY[i]: # line 3
            tableT[t] = i
        tableS[i]='' #line 4
    for i in range(len(partitionZ)): # line 5
        for t in partitionZ[i]: # line 6
            if ( not (tableT[t] == 'NULL')): # line 7
                tableS[tableT[t]] = sorted(list(set(tableS[tableT[t]]) | set([t])))
        for t in partitionZ[i]: # line 8
            if (not (tableT[t] == 'NULL')) and len(tableS[tableT[t]])>= 2 : # line 9
                partitionofx.append(tableS[tableT[t]])
            if not (tableT[t] == 'NULL'): tableS[tableT[t]]='' # line 10
    for i in range(len(partitionY)): # line 11
        for t in partitionY[i]: # line 12
            tableT[t]='NULL'
    dictpartitions[''.join(sorted(x))] = partitionofx#生成属性集X上的剥离分区
    print('x=%s,partitionX=%s'%(x,partitionofx))

def computeSingletonPartitions(listofcols):
    global data2D
    global dictpartitions
    for a in listofcols:
        dictpartitions[a]=[]
        for element in list_duplicates(data2D[a].tolist()): # list_duplicates returns 2-tuples, where 1st is a value, and 2nd is a list of indices where that value occurs
            if len(element[1])>1: # 忽略单例等价类
                dictpartitions[a].append(element[1])
