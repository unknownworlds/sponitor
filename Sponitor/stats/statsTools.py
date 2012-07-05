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



    

