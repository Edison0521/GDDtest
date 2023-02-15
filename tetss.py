import numpy as np
import pandas as pd
import time
import itertools
import Levenshtein as ls
import re
def ass(s):
    a = 1
    b = 2
    return a,b


L = [0,1,2,5,4]
class Dtems(object):
    def __init__(self, itemname, newname, items):
        self.name = itemname
        self.newname = newname
        self.sigma = items

    def __repr__(self):
        return "%s %s %s" % (self.name, self.sigma, self.newname)

for i in range(len(L)):
    if L[i] == i:
        print(L[i])
class node_s(object):
    def __init__(self, id, name, attribute):
        self.id = id
        self.name = name
        self.attribute = attribute

    def __repr__(self):
        return "%s %s %s" % (self.id, self.name, self.attribute)

def namelist(name):
    name = name.strip('=')
    return name

s = '(0:x0).Name=EA'
print(namelist(s))