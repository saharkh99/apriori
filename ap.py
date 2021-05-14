import csv
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# analysis of

def getTransListSet(filePath='groceries.csv'):
    # get file.csv
    transListSet = []
    with open(filePath, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader:
            transListSet.append(set(line))
    return transListSet


if __name__ == '__main__':

    df = getTransListSet()
    localSetForCounts = defaultdict(int)
    itemSet = set()
    for line in df:
        for item in line:
            if str(item):
                itemSet.add(frozenset([item]))
    for item in itemSet:
        localSetForCounts[item] += sum([1 for trans in df if item.issubset(trans)])
    df = pd.DataFrame(list(localSetForCounts.items()), columns=['product', 'count'])
    print("most sold products")
    t=df.sort_values(ascending=0, by='count')[:10]
    print(t)
    print("least sold products")
    l=df.sort_values(ascending=0, by='count')[-10:]
    print(l)
    print("mean: "+str(df['count'].mean()))
    # plt.stem(df['product'].apply(lambda x: list(x)[0]).astype("unicode"),df['count'].sort_values())
    df1=df.sort_values(ascending=0,by='count')[:10].plot.bar(x='product', y='count', rot=0, align='edge', width=0.4,fontsize=5)
    # df.boxplot('count')
    plt.interactive(False)
    plt.figure(figsize=(50, 3))
    plt.show()
