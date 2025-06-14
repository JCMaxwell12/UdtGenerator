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
            'amount':   arySize,
            'bytePos':  0
        })

reservedCnt = 0
udtSize = 0
for attribute in attributes:     # Convert names to Pascal Case
    attribute['name'] = toPascalCase(attribute['name'])

    if attribute['name'] == '':  # Change names to ReservedN
        attribute['name'] = f'Reserved{reservedCnt}'
        reservedCnt += 1

    sizeOfAttribute = dataTypes[attribute['type']]['size'] * attribute['amount']
    if attribute['type'] == 'string':      # Strings have a length
        sizeOfAttribute = sizeOfAttribute * attribute['size']

    attribute['bytePos'] = f'{int(udtSize / 8)}.{udtSize % 8}'
    udtSize += sizeOfAttribute

    prefix = ''
    if reservedPrefix != '' and attribute['name'].startswith('Reserved'):
        prefix = reservedPrefix
    if addPrefix:   # Preppend names with their data type abbreviation
        if attribute['amount'] > 1:  # Handle arrays
            prefix += 'a'
        else:
            prefix += dataTypes[attribute['type']]['abbrev']

    attribute['name'] = prefix + attribute['name']

hasDuplicates = findDupes(attributes, 'name')
if hasDuplicates[0]:
    raise Exception(hasDuplicates[1])

with open('udt.csv', 'w', newline='') as udtFile:   # Write to file
    csvWriter = csv.writer(udtFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvWriter.writerow(['Byte.bit', 'Name', 'Data type'])
    for attribute in attributes:
        attrName = attribute['name']
        dataType = attribute['type']
        bytePos = attribute['bytePos']
        if attribute['type'] == 'string':    # Handle string size
            dataType = f'string[{attribute['size']}'

        if attribute['amount'] > 1:  # Handle arrays
            dataType = f'Array [0..{attribute['amount'] - 1}] of {dataType}'

        csvWriter.writerow([bytePos, attrName, dataType])

print(f'Size of UDT (bits): {udtSize}')
print(f'Size of UDT (Bytes.bits): {int(udtSize / 8)}.{udtSize % 8}')
print(f'Size of UDT (Words.bits): {int(udtSize / 16)}.{udtSize % 16}')
