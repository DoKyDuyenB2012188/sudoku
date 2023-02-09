def convertStrToGrid(gridStr):
    parseGrid = []
    loop = 0
    row = []
    for i in range(0, 81):
        if gridStr[i] == '0':
            row.append(0)
        else:
            row.append(int(gridStr[i]))
        loop += 1
        if loop % 9 == 0:
            parseGrid.append(row)
            row = []
    return parseGrid
