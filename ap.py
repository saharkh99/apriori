import csv
from collections import defaultdict

def getTransListSet( filePath='x.csv'):
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
            itemSet.add(frozenset([item]))
    return itemSet

def fillItemCountDict(itemSet,transListSet):
    localSet_ = defaultdict(int)
    for item in itemSet:
        localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])
        print(item)
    return localSet_


def getJoinedItemSet(termSet, k):
    return set([term1.union(term2) for term1 in termSet for term2 in termSet
                if len(term1.union(term2))==k])

def getSupport(itemCount,transLength):
    print(itemCount)
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


def checkConfidence(itemCountDict,minConf):
    rules = dict()
    for key, value in itemCountDict.items():
        for item in value:
            item_supp = getSupport(item)
            conf = item_supp / getSupport(item)
            if conf >= minConf:
                rules[item] = conf
    return rules


if __name__ == '__main__':
    itemCountDict = defaultdict(int)
    transLength = len(getTransListSet())
    itemSet = getOneItemSet(getTransListSet())
    itemCountDict=fillItemCountDict(itemSet,getTransListSet())
    print(getJoinedItemSet(itemSet,1))
    print(getSupport(itemCountDict[frozenset({'whole milk'})],transLength))
    print(getTransListSet(),itemSet,2)