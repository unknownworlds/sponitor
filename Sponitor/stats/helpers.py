import math

def quantiles(n, series):
    series        = sorted(series)
    quantiles     = []
    quantileIndex = 1
    next          = math.floor(float(quantileIndex * len(series)) / n)   

    for i, data in enumerate(series):
        if i == next:
            quantiles.append(data)

            quantileIndex += 1
            next = math.floor(float(quantileIndex * len(series)) / n)

    return quantiles

def findCategory(time, delta, iMax, unit = '', offset = 0):
    i = int(math.floor( (time - offset)/delta))
    
    if i < 0:
        i = -1
        name = '<' + str(int(offset)) + unit
    elif i >= iMax:
        i = int(iMax)
        name = '>' + str(i * delta) + unit
    else:    
        name = str(i * delta + offset) + unit + '-' + str((i+1) * delta + offset) + unit
    
    return i, name

