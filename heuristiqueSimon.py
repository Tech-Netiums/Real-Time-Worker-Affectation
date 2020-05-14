# -*- coding: utf-8 -*-
"""
Created on Thu May  7 09:06:54 2020

@author: simon
"""

from objet import Worker, Machine

def heuristique_simon1(Machines_available, worker, Workers) :
    other_workers = []
    #1. Pour chaque machine, regarder les travailleurs qui peuvent travailler dessus
    for k in range(len(Machines_available)) :  
        other_workers_machinek = []
        for i in range(len(Workers)) :
            if Workers[i].skills[k] == 1 and i+1 != worker.number :
                other_workers_machinek.append(Workers[i])
        other_workers.append(other_workers_machinek)
        
    #2. Pour chaque machine, comparer le niveau de fatigue des workers
    print(other_workers)
    workers_fatigue =[]
    for k in range(len(Machines_available)) :
        fatigue = []
        for qualified_worker in other_workers[k] :
            fatigue.append(worker.fatigue - qualified_worker.fatigue)      
        workers_fatigue.append(fatigue)
        
    #3. On choisit la machine pour lequel le worker est le plus en forme
    print(workers_fatigue)
    difference_min = workers_fatigue[0][0]
    index_machine = 0
    for k in range(len(Machines_available)) :
        for i in range(len(other_workers[k])) :
            if workers_fatigue[k][i] < difference_min :
                difference_min = workers_fatigue[k][i]
                index_machine = k
   
    #4. On renvoit l'indice de la machine
    return index_machine