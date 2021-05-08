import csv
import itertools
from collections import defaultdict


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
        l = [x for x in item]
        localSet_[str(l)] += sum([1 for trans in transListSet if item.issubset(trans)])
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


def getCombinations(freqSe, itemCountDict,min_confidence,lentrans):
    rules=[]
    lifts=[]
    lift=1
    for r in freqSe:
        perm = itertools.permutations(r)
        for i in perm:
            li = list(i)
            temp_i = li[:]
            for j in range(len(li) - 1):
                k = [x for index, x in enumerate(temp_i) if index <= j]
                m = [x for x in li if x not in k]
                b1 = getSupport(itemCountDict[str(k)], lentrans)
                b2 = getSupport(itemCountDict[str(temp_i)], lentrans)
                b3 = getSupport(itemCountDict[str(m)], lentrans)
                if(b3*b1!=0):
                   lift= b2/b1*b3
                if (b2 != 0):
                    confidence = b1 / b2
                    if (confidence >= min_confidence):
                        elm=str(k) + "->" + str(m)
                        if(elm!=None):
                           lifts.append(lift)
                           rules.append(elm)
    dicta=dict(zip(rules,lifts))
    [print(key, value) for (key, value) in sorted(dicta.items(), key=lambda x: x[1])]
def getTransListSet(filePath='groceries.csv'):
        transListSet = []
        with open(filePath, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for line in reader:
                transListSet.append(set(line))
        return transListSet
class Arules:
    dicta = defaultdict(int)
    l = []
    def get_frequent_item_sets(self,transactions=getTransListSet(),min_support=0.005, min_confidence=0.2):
        freqSet = dict()
        itemCountDict = defaultdict(int)
        transLength = len(transactions)
        itemSet = getOneItemSet(transactions)
        itemCountDict = fillItemCountDict(itemSet, transactions)
        freqOneTermSet = getItemsWithMinSupp(transactions, itemSet, min_support)
        k = 1
        self.dicta.update(itemCountDict)
        currFreqTermSet = dict()
        currFreqTermSet = freqOneTermSet
        self.l.append([list(x) for x in currFreqTermSet])
        while currFreqTermSet != set():
            freqSet[k] = currFreqTermSet
            k += 1
            currCandiItemSet = getJoinedItemSet(currFreqTermSet, k)
            currFreqTermSet = getItemsWithMinSupp(transactions, currCandiItemSet,min_support)
            itemCountDict = fillItemCountDict(currFreqTermSet, transactions)
            self.dicta.update(itemCountDict)
            if(len(currFreqTermSet)>0):
              self.l.append([list(x) for x in currFreqTermSet])
        return self.l

    def get_arules(self, min_support=0.005, min_confidence=0.2,min_lift=None,sort_by='lift'):
         self.get_frequent_item_sets()
         for i in self.l:
             if(i!=None):
                getCombinations(i, self.dicta, min_confidence, len(getTransListSet()))