#!/usr/bin/env python3
# vim: set ai et ts=4 sw=4:
from typing import List

import matplotlib as mpl
import matplotlib.pyplot as plt
import math

import numpy as np


class Graph:
    delta=0
    dx = 0.01
    y = []
    def __init__(self,arguments: List[List[float]],
                 results: List[float],
                 appro,
                 degree: int,
                 name ):
        self.x=[]
        for e in arguments:
            self.x+=e
        self.y = results
        self.apro = appro
        self.degree = degree
        self.name = name

    def func(self,x):
        result=0
        pow = 0
        for e in self.apro.coef:
            result += e*math.pow(x,pow)
            pow+=1
        return result
    def draw(self):
        dpi = 80
        fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
        mpl.rcParams.update({'font.size': 10})



        # plt.xlabel('x')
        # plt.ylabel('F(x)')


        num = 0
        for x in self.x:

            q = math.fabs(self.func(x) - self.y[num])
            if q >self.delta:
                self.delta = q
            num += 1
        plt.scatter(self.x,self.y, color = 'blue', label = u'points')
        min=self.x[0]
        max=self.x[self.x.__len__()-1]
        self.x=[]
        self.y=[]
        for num in np.arange(min,max,0.01):
            self.x+=[num]
            self.y+=[self.func(num)]


        plt.grid()

        plt.plot(self.x, self.y, color = 'red', label = "result")
        plt.legend(loc = 'upper right')
        plt.suptitle(self.name)
        plt.title("Точность: " + str(math.fabs(self.delta)))
        fig.savefig(str(self.degree) +'.png')
