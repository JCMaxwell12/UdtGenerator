import csv

units = []

with open('definition.csv') as def_file:
    deflines = csv.reader(def_file, delimiter=',')
    if deflines.line_num < 1:
        raise Exception('Empty definition file')

    for row in deflines:
        if row == ['Name', 'Type', 'Size', 'Amount']:
            continue

        units.append({
                'name':     row[0],
                'type':     row[1],
                'size':     row[2],
                'amount':   row[4]
        })



