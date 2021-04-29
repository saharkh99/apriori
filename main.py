import csv


def read_data(file_loc='groceries.csv'):
    data = dict()
    with open(file_loc) as f:
        filedata = csv.reader(f, delimiter=',')
        count = 0
        for line in filedata:
            count += 1
            data[count] = list(set(line))
    return data

if __name__ == '__main__':
    print(read_data())

