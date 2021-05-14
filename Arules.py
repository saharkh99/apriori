import csv
import itertools
from collections import defaultdict
from matplotlib import pyplot as plot
import statistics


def getOneItemSet(transListSet):
    # get all the transactions and save it in itemSet
    itemSet = set()
    for line in transListSet:
        for item in line:
            if len(str(item)) != 0:
                itemSet.add(frozenset([item]))
    return itemSet


def fillItemCountDict(itemSet, transListSet):
    # set dictionary with items and their counts
    localSetForCounts = defaultdict(int)
    for item in itemSet:
        l = [x for x in item]
        perm = itertools.permutations(l)
        for i in perm:
            localSetForCounts[str(list(i))] += sum([1 for trans in transListSet if item.issubset(trans)])
    return localSetForCounts


def getJoinedItemSet(termSet, k):
    # join terms to make k-term
    return set([term1.union(term2) for term1 in termSet for term2 in termSet
                if len(term1.union(term2)) == k])


def getSupport(itemCount, transLength):
    # support for term
    return itemCount / transLength


def getItemsWithMinSupp(transListSet, itemSet, minSupp):
    # compare with min support in each itemset
    itemSet_ = set()
    localSet_ = defaultdict(int)
    for item in itemSet:
        localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])
    n = len(transListSet)
    for item, count in localSet_.items():
        itemSet_.add(item) if float(count) / n >= minSupp else None
    return itemSet_


def getRules(freqSe, itemCountDict, min_confidence, lentrans):
    # make rules(k->m) from frequent itemSets with this pattern:temp_i{k,m}
    # {k,m}
    rules = []
    lifts = []
    lift = 1
    for r in freqSe:
        perm = itertools.permutations(r)
        for i in perm:
            li = list(i)
            temp_i = li[:]
            for j in range(len(li) - 1):
                k = [x for index, x in enumerate(temp_i) if index <= j]
                m = [x for x in li if x not in k]
                support_k = getSupport(itemCountDict[str(k)], lentrans)
                support_total = getSupport(itemCountDict[str(temp_i)], lentrans)
                support_m = getSupport(itemCountDict[str(m)], lentrans)
                if (support_k != 0):
                    confidence = support_total / support_k
                    if (support_m != 0):
                        lift = confidence / support_m
                    if (confidence >= min_confidence):
                        elm = str(k) + "->" + str(m) + " , " + str(lift)
                        if (elm != None):
                            lifts.append(lift)
                            rules.append(elm)
    dicta = dict(zip(rules, lifts))
    return dicta
    # [print(key) for (key, value) in sorted(dicta.items(), key=lambda x: x[1], reverse=True)]


def getTransListSet(filePath='groceries.csv'):
    # get file.csv
    transListSet = []
    with open(filePath, 'r') as file:
        readerCSV = csv.reader(file, delimiter=',')
        for line in readerCSV:
            transListSet.append(set(line))
    return transListSet


class Arules:
    dicta = defaultdict(int)
    l = []

    def get_frequent_item_sets(self, transactions=getTransListSet(), min_support=0.005):
        # initial itemCountdict and freqOneSet for k=1
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
        # increase the number of k for joining k items until  there is no item in set
        while currFreqTermSet != set():
            freqSet[k] = currFreqTermSet
            k += 1
            currCandiItemSet = getJoinedItemSet(currFreqTermSet, k)
            currFreqTermSet = getItemsWithMinSupp(transactions, currCandiItemSet, min_support)
            itemCountDict = fillItemCountDict(currFreqTermSet, transactions)
            self.dicta.update(itemCountDict)
            if (len(currFreqTermSet) > 0):
                self.l.append([list(x) for x in currFreqTermSet])
        return self.l

    def get_arules(self, min_support=0.3, min_confidence=0.2, min_lift=None, sort_by='lift'):
        self.get_frequent_item_sets()
        dicta1 = dict()
        for i in self.l:
            if (i != None):
                dicta1.update(getRules(i, self.dicta, min_confidence, len(getTransListSet())))
        pre_value = 0
        for (key, value) in sorted(dicta1.items(), key=lambda x: x[1], reverse=True):
            if (pre_value != value):
                [print(key)]
                pre_value = value
