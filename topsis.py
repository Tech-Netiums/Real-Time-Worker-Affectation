# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:13:57 2020

@author: simon
"""

import math
import numpy as np
import random
from parameters import delta, nu
from objet import Worker, Machine


def topsis(Machines_available, worker) : 
# On construit dans un premier temps la matrice A
    A = np.zeros((len(Machines_available),2))
    for i in range(len(Machines_available)) :
        machine = Machines_available[i]
        #Critère C1 : SPT
        initial_duration = machine.time_queue[0]
        penibility = machine.penibility
        exact_duration = initial_duration * ( 1 + delta * penibility * (math.log(1 + worker.fatigue) ))
        A[i][0] = exact_duration
        
        #Critère C2 : LNQ 
        queue = machine.queue
        lower_bound_fatigue = worker.fatigue + (1 - worker.fatigue)*(1 - math.exp(-penibility*exact_duration))
        for j in range(len(queue)-1) : 
            initial_duration = machine.time_queue[j+1]
            additional_duration = initial_duration * ( 1 + delta * penibility * (math.log(1 + lower_bound_fatigue) ))
            exact_duration += additional_duration
            lower_bound_fatigue += (1 - lower_bound_fatigue)*(1 - math.exp(-penibility*additional_duration))
        A[i][1] = exact_duration
        
    # On normalise et on pondère cette matrice 
    V = np.zeros((len(Machines_available),2))
    for j in range(2) :
        norm = 0
        for i in range(len(Machines_available)) :
            norm +=  A[i][j]
        norm = math.sqrt(norm)
        for i in range(len(Machines_available)) :
            V[i][j] = nu[j]*A[i][j]/norm

    #Détermination de la pire et de la meilleure alternative
    min_C = [V[0][0], V[0][1]]
    max_C = [V[0][0], V[0][1]]
    for i in range(len(Machines_available)) :
        for j in range(2) :
            if V[i][j] < min_C[j] :
                min_C[j] = V[i][j]
            elif V[i][j] > max_C[j] : 
                max_C[j] = V[i][j]
                
    #ideal solution
    IA = [max_C[1], min_C[0]]
    #worst solution
    WA = [max_C[0], min_C[1]]
    
    #Mesure de la distance euclidienne 
    IS = []
    WS = []
    for j in range(len(Machines_available)) : 
        ISj = math.sqrt((V[j][0] - IA[0])**2 + (V[j][1] - IA[1])**2)
        WSj = math.sqrt((V[j][0] - WA[0])**2 + (V[j][1] - WA[1])**2)
        IS.append(ISj)
        WS.append(WSj)
        
    #Calcul de la similitude avec les pires conditions
    S = []
    for j in range(len(Machines_available)) : 
        S.append(IS[j]/(IS[j]+WS[j]))
    
    #Détermination du ratio max 
    maxS = S[0]
    machine_index = 0
    for j in range(len(Machines_available)) :
        if S[j] > maxS :
            maxS = S[j]
            machine_index = j
    return machine_index



    