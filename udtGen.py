import csv


def findDupes(dictsList, testKey):
    for dictX in range(len(dictsList)):
        for dictY in range(dictX+1, len(dictsList)):
            if dictsList[dictX][testKey] == dictsList[dictY][testKey]:
                return True, f'{dictsList[dictX][testKey]} is duplicate in positions {dictX}, {dictY}'
    return False, ''


def toPascalCase(string):
    return string.title().replace(' ', '')


addPrefix = True
reservedPrefix = '_'


dataTypes = {}
with open('dataTypes.csv') as def_file:
    deflines = csv.reader(def_file, delimiter=',')

    for row in deflines:
        dataTypes.update({
            row[0]: {
                'size':     int(row[1]),
                'abbrev':   row[2]
            }})

attributes = []
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

        attributes.append({
            'name':     row[0],
            'type':     dType,
            'size':     size,
            'amount':   arySize
        })

reservedCnt = 0
udtSize = 0
for i in range(len(attributes)):     # Convert names to Pascal Case
    attrName = attributes[i]['name']
    attributes[i]['name'] = toPascalCase(attrName)

    if attributes[i]['name'] == '':  # Change names to ReservedN
        attributes[i]['name'] = f'Reserved{reservedCnt}'
        reservedCnt += 1

    sizeOfAttribute = dataTypes[attributes[i]['type']]['size'] * attributes[i]['amount']
    if attributes[i]['type'] == 'string':      # Strings have a length
        sizeOfAttribute = sizeOfAttribute * attributes[i]['size']

    udtSize += sizeOfAttribute

    prefix = ''
    if addPrefix:   # Preppend names with their data type abbreviation
        if attributes[i]['amount'] > 1:  # Handle arrays
            prefix = 'a'
        else:
            prefix = dataTypes[attributes[i]['type']]['abbrev']
    if reservedPrefix != '' and attrName.startswith('Reserved'):
        prefix = '_'

    attributes[i]['name'] = prefix + attrName

hasDuplicates = findDupes(attributes, 'name')
if hasDuplicates[0]:
    raise Exception(hasDuplicates[1])

with open('udt.csv', 'w', newline='') as udtFile:   # Write to file
    csvWriter = csv.writer(udtFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvWriter.writerow(['Name', 'Data type'])
    for attribute in attributes:
        attrName = attribute['name']
        dataType = attribute['type']
        if attribute['type'] == 'string':    # Handle string size
            dataType = f'string[{attribute['size']}'

        if attribute['amount'] > 1:  # Handle arrays
            dataType = f'Array [0..{attribute['amount'] - 1}] of {dataType}'

        csvWriter.writerow([attrName, dataType])
