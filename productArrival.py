# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:30:00 2020

@author: simon
"""

import numpy as np

lam = [[0.7,0.02,0.08,0.2,0.035,0.015,0.065,0.3,0.025,0.085,0.04],
       [0.04,0.05,0.1,0.04,0.1,0.4,0.075,0.1,0.05,0.3,0.06],
       [0.04,0.04,0.8,0.04,0.03,0.1,0.03,0.2,0.07,0.1,0.5],
       [0.04,0.2,0.,0.1,0.03,0.3,0.5,0.4,0.015,0.,0.07]]

def next_arrival(id_product, time) : 
    index = int(time/60)
    m = lam[id_product][index+1] - lam[id_product][index] #coeff directeur de la droite
    p = lam[id_product][index] - m*index
    lamb = m*time/60 + p
    return np.random.exponential(1/lamb)

time_limit = 60*8

product_arrival = [[],[],[],[]]

for i in range(4) : 
        time = 0.
        while time < time_limit :
            new_arrival = next_arrival(i,time)
            time += new_arrival
            product_arrival[i].append(time)