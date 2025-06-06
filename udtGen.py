import csv

def findDupes(dictsList, testKey):
    for i in range(len(dictsList)):
        for dictn in range(i+1, len(dictsList)):
            if dictsList[i][testKey] == dictsList[dictn][testKey]:
                return True, f'{dictsList[i][testKey]} is duplicate in positions {i}, {dictn}'
    return False, ''

def toPascalCase(string):
    return string.title().replace(' ', '')


dataTypes = {}
with open('dataTypes.csv') as def_file:
    deflines = csv.reader(def_file, delimiter=',')

    for row in deflines:
        dataTypes.update({
                row[0]: {
                'size':     int(row[1]),
                'abbrev':   row[2]
            } })

units = []
with open('definition.csv') as def_file:
    deflines = csv.reader(def_file, delimiter=',')

    for row in deflines:
        if row == ['Name', 'Type', 'Size(str)', 'ArraySize']:
            continue

        dType = row[1].strip().lower()
        if not dType in dataTypes:
            raise Exception(f'Data type {dType} not found')

        size = 1
        try:
            size = int(row[2])
        except ValueError:   # if row[2[ is not a number keep it a 1
            pass

        arySize = 1
        try:
            arySize = int(row[3])
        except ValueError:   # if row[3] is not a number keep it a 1
            pass

        units.append({
                'name':     row[0],
                'type':     dType,
                'size':     size,
                'amount':   arySize
        })

reservedCnt = 0
udtSize = 0
for i in range(len(units)):     # Convert names to Pascal Case
    units[i]['name'] = toPascalCase(units[i]['name'])

    if units[i]['name'] == '':  # Change names to ReservedN
        units[i]['name'] = f'Reserved{reservedCnt}'
        reservedCnt += 1
    
    sizeOfUnit = dataTypes[units[i]['type']]['size'] * units[i]['amount']
    if units[i]['type'] == 'string':      # Strings have a length
        sizeOfUnit = sizeOfUnit * units[i]['size']

    udtSize += sizeOfUnit

hasDuplicates = findDupes(units, 'name')
if hasDuplicates[0]:
    raise Exception(hasDuplicates[1])


for i in range(len(units)):     # Preppend names with their data type abbreviation
    if units[i]['amount'] > 1:  # Handle arrays
        units[i]['name'] = 'a' + units[i]['name']
    else:
        units[i]['name'] = dataTypes[units[i]['type']]['abbrev'] + units[i]['name']


with open('udt.csv', 'w', newline='') as udtFile:
    csvWriter = csv.writer(udtFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvWriter.writerow(['Name', 'Data type'])
    for unit in units:     # Preppend names with their data type abbreviation
        varName = unit['name']
        dataType = unit['type']
        if unit['type'] is 'string':    # Handle string size
            dataType = f'string[{unit['size']}'

        if unit['amount'] > 1:  # Handle arrays
            dataType =  f'Array [0..{unit['amount'] - 1}] of {dataType}'

        csvWriter.writerow([varName, dataType])
