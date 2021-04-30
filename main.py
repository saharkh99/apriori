import csv


def read_data(file_loc='x.csv'):
    data = dict()
    with open(file_loc) as f:
        filedata = csv.reader(f, delimiter=',')
        count = 0
        for line in filedata:
            count += 1
            data[count] = list(set(line))
    return data

def frequence(trans,items_lst):
    c=0
    s=""
    items_counts = dict()
    for i in items_lst:
        s +=i + ","
    for j in trans.items():
        for i in items_lst:
            if i not in j[1]:
                break;
            else:
                print(i)
                c += 1
        if (c == len(items_lst)):
            if i in items_counts:
                items_counts[s] += 1
                print(items_counts)
            else:
                items_counts[s] = 1
        c=0
    return items_counts

def association_rules(items_grater_then_min_support):
    rules = []
    c=0
    dict_rules = {}
    for i in items_grater_then_min_support:
       for j in items_grater_then_min_support:
           rules.append(i)
           rules.append(j)
       dict_rules[c] =rules
       rules=[]
def association_rules2(items_grater_then_min_support):
    rules = []
    dict_rules = {}
    for i in items_grater_then_min_support:
        dict_rules = {}
        if type(i) != type(str()):
            i = list(i)
            temp_i = i[:]
            for j in range(len(i)):
                k = temp_i[j]
                del temp_i[j]
                dict_rules[k] = temp_i
                temp_i = i[:]
        rules.append(dict_rules)
    temp = []
    for i in rules:
        for j in i.items():
            if type(j[1]) != type(str()):
                temp.append({tuple(j[1])[0]: j[0]})
            else:
                temp.append({j[1]: j[0]})
    rules.extend(temp)
    return rules




def frequence2(items_lst, trans, check=False):
    items_counts = dict()
    for i in items_lst:
        temp_i = {i}
        if check:
            temp_i = set(i)
        for j in trans.items():
            if temp_i.issubset(set(j[1])):
                if i in items_counts:
                    items_counts[i] += 1
                else:
                    items_counts[i] = 1
    return items_counts
def support(items_counts, trans):
    support = dict()
    total_trans = len(trans)
    for i in items_counts:
        support[i] = items_counts[i]/total_trans
    return support[i]

if __name__ == '__main__':
    print(read_data())
    print(support(frequence(read_data(),['yogurt','coffee']),read_data()))
    print(support(frequence2(['yogurt','coffee'],read_data()),read_data()))
    print(frequence2(['yogurt','coffee'],read_data()))
    print(association_rules(['yogurt','coffee']))