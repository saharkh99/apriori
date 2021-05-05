import csv
import itertools
from collections import defaultdict

import options as options


def getTransListSet(filePath='x.csv'):
    transListSet = []
    with open(filePath, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader:
            transListSet.append(set(line))
    return transListSet


def getOneItemSet(transListSet):
    itemSet = set()
    for line in transListSet:
        for item in line:
            if str(item):
                itemSet.add(frozenset([item]))
    return itemSet


def fillItemCountDict(itemSet, transListSet):
    localSet_ = defaultdict(int)
    for item in itemSet:
        localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])
        # print(item)
    return localSet_


def getJoinedItemSet(termSet, k):
    return set([term1.union(term2) for term1 in termSet for term2 in termSet
                if len(term1.union(term2)) == k])


def getSupport(itemCount, transLength):
    return itemCount / transLength


def getItemsWithMinSupp(transListSet, itemSet, minSupp):
    itemSet_ = set()
    localSet_ = defaultdict(int)
    for item in itemSet:
        localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])
    n = len(transListSet)
    for item, cnt in localSet_.items():
        itemSet_.add(item) if float(cnt) / n >= minSupp else None

    return itemSet_


def checkConfidence(itemCountDict, minConf, tranlen):
    rules = dict()
    for key, value in itemCountDict.items():
        item_supp = getSupport(value, tranlen)
        for item in key:
           conf = item_supp / getSupport(itemCountDict[item], tranlen)
           if conf >= minConf:
               rules[key] = conf
    return rules

def getCombinations(freqSe):
    perm=[]
    dict_rules=dict()
    li=[]
    x=0
    for r in freqSe:
        perm = itertools.permutations(r)
        for i in perm:
           li=list(i)
           temp_i = li[:]
           for j in range(len(li)-1):
               k = [x for index, x in enumerate(temp_i) if index <= j]
               m = [x for x in li if x not in k]
               print(str(k)+"->"+str(m))
if __name__ == '__main__':
    freqSet = dict()
    itemCountDict = defaultdict(int)
    transLength = len(getTransListSet())
    itemSet = getOneItemSet(getTransListSet())
    itemCountDict = fillItemCountDict(itemSet, getTransListSet())
    freqOneTermSet = getItemsWithMinSupp(getTransListSet(), itemSet, 0.005)
    k = 1
    currFreqTermSet = dict()
    l=[]
    currFreqTermSet = freqOneTermSet
    # l.append([list(x) for x in currFreqTermSet])
    while currFreqTermSet != set():
        freqSet[k] = currFreqTermSet
        k += 1
        currCandiItemSet = getJoinedItemSet(currFreqTermSet, k)
        currFreqTermSet = getItemsWithMinSupp(getTransListSet(), currCandiItemSet, 0.005)
        itemCountDict = fillItemCountDict(currFreqTermSet, getTransListSet())
        # print(itemCountDict.items())
        # print("frequent item sets")
        # print()
        l.append([list(x) for x in currFreqTermSet])

        # print("confidence with rules")
        # print(checkConfidence(itemCountDict, 0.2, transLength))
# confidence- lift
    for i in l:
       print(getCombinations(i))