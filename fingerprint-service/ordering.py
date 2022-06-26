import csv

keys = {}

with open('fingerprints.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')

    for row in csv_reader:
        del row[len(row)-1]
        del row[0]

        if row[0] in keys.keys():
            keys[row[0]].append(row)
        else:
            keys[row[0]] = [row]
    
    f = open('ordered_fingerprints.csv', 'w')
    writer = csv.writer(f)
    for key in keys.keys():
        for row in keys[key]:
            writer.writerow(row)

    f.close()
    
    #print(row)