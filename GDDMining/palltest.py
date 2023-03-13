import pandas as pd
import multiprocessing as mp
import numpy as np
import time
import itertools
import Levenshtein as ls
import re
import copy
from itertools import combinations
import operator
import glob
from GDDMining import GDD

def block(title,items,seg):
    print(title,items)


def count_distinct_values(column, df):
    # 统计一列中不同的值
    distinct_values = {}
    for index, value in enumerate(df[column]):
        if value not in distinct_values:
            distinct_values[value] = []
        distinct_values[value].append(index)
    return (column, distinct_values)

if __name__ == '__main__':
    # 读取数据
    #df = pd.read_csv('data.csv')
    filename = 'produce_Table0.txt'
    files = filename + 'result40.txt'
    df = pd.read_csv(filename, delimiter=";;", engine='python')

    # 创建进程池
    pool = mp.Pool()

    # 并行统计每一列中不同的值
    results = []
    for column in df.columns:
        result = pool.apply_async(count_distinct_values, args=(column, df))
        results.append(result)

    # 等待所有进程结束并收集结果
    distinct_values = {}
    for result in results:
        column, values = result.get()
        distinct_values[column] = values

    # 打印结果
    '''for column, values in distinct_values.items():
        print(f"列 {column} 中不同的值有：")
        for value, rows in values.items():
            print(f"\t{value}：{rows}")'''
    #cloumns = []
    #for val in distinct_values
    title = []
    for cloum_name in df.columns:
        title.append(df[cloum_name].name)
    con = 1
    starttime = time.time()
    thresord = int(con * len(df))
    candite = []  # contains the every attribute with it items
    #pure_list = ['id']
    # print(title)
    relation_candait = []
    #print(distinct_values[title[0]])
    for item in title:
        if 'id' not in item:
            # print("How many different distances do you want about", title[i])
            # seg = int(input())
            seg = 3
            b = block(item,distinct_values[item],seg)
            #x = relationbolck(item, seg)
            #relation_candait.append(x)
            #x =
        elif 'id' in item:
            seg = 1
            #x = relationbolck(item, seg)
            #relation_candait.append(x)
