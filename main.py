import random

import numpy as np

from approximation import Approximation
import json
import math
from draw import Graph

xs = []
# ys = [30, 25, 16, -1, 10, 5, 0, 10, 4, 9, 16, -2, 9]

name = "Y=X²-6"

if __name__ == '__main__':

    ys = []
    num = 0
    for x in range(-10,11):
        if random.randint(1,100)<60:
            temp = [x]
            xs.append([])
            xs[num]=(temp)
            ys += [x*x-6]
            num+=1
    for degree in range(2,13):

        approximation = Approximation.fit(xs,ys,degree)

        graph = Graph(xs,ys,approximation,degree, name)
        graph.draw()

    data = {
        "data": {
            "coef": approximation.coef,
            "names": approximation.names,
            "json": approximation.json,
            "latex": approximation.latex,
        }
    }
    with open('data.json', 'w') as outfile:
        json.dump(data,outfile)

    print(approximation.latex)
