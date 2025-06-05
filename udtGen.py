import csv

def findDupes(dictsList, testKey):
    for i in range(len(dictsList)):
        for dictn in range(i+1, len(dictsList)):
            if dictsList[i][testKey] == dictsList[dictn][testKey]:
                return True, f'{dictsList[i][testKey]} is duplicate in positions {i}, {dictn}'
    return False, ''

def toPascalCase(string):
    return string.title().replace(' ', '')

units = []

with open('definition.csv') as def_file:
    deflines = csv.reader(def_file, delimiter=',')

    for row in deflines:
        if row == ['Name', 'Type', 'Size', 'Amount']:
            continue

        units.append({
                'name':     row[0],
                'type':     row[1],
                'size':     row[2],
                'amount':   row[3]
        })

dataTypes = {}
with open('dataTypes.csv') as def_file:
    deflines = csv.reader(def_file, delimiter=',')

    for row in deflines:
        dataTypes.update({
                row[0]: {
                'size':     row[1],
                'abbrev':   row[2]
            } })

reservedCnt = 0
for i in range(len(units)):     # Convert names to Pascal Case
    units[i]['name'] = toPascalCase(units[i]['name'])

    if units[i]['name'] == '':  # Change names to ReservedN
        units[i]['name'] = f'Reserved{reservedCnt}'
        reservedCnt += 1

hasDuplicates = findDupes(units, 'name')
if hasDuplicates[0]:
    raise Exception(hasDuplicates[1])


