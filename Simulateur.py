# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:30:22 2020

@author: louis
"""
import random 
import math
import numpy as np
from termcolor import colored

delta = 0.3

class Product : 
    def __init__(self, number, path, duration):
        self.number = number
        self.path = path 
        self.duration = duration 
        self.arrivals = []
        self.departures = []
        
        
Product1 = Product(1, [1,2,3,4,8], [[14,17], [5,8], [28,32], [2,4], None, None, None, [30,37]])
Product2 = Product(2, [2,4,7], [None, [10,13], None, [20,25], None, None, [6,8], None ])
Product3 = Product(3, [3,5,1], [[25,28], None, [5,10], None, [10,14], None, None, None])
Product4 = Product(4, [5,6,7,8], [None, None, None, None, [5,9], [12,15], [30,34], [3,7]])

Products = [Product1, Product2, Product3, Product4]

class Worker :
    def __init__(self, number,  Skills): 
        self.number = number 
        self.skills = Skills
        self.fatigue = 0
        
    def increase_fatigue(self, new_fatigue_level): 
        self.fatigue = new_fatigue_level
    
Worker1 = Worker(1, [1, 1, 0, 0, 0, 0, 0, 0])
Worker2 = Worker(2, [0, 0, 1, 1, 0, 0, 0, 0])
Worker3 = Worker(3, [0, 0, 0, 0, 1, 1, 0, 0])
Worker4 = Worker(4, [0, 0, 0, 0, 0, 0, 1, 1])

Workers = [Worker1, Worker2, Worker3, Worker4]


class Machine : 
    def __init__(self, number, penibility):
        self.number = number
        self.queue = []
        self.occupation = 0
        self.penibility = penibility
        
Machine1 = Machine(1, 0.8)
Machine2 = Machine(2, 0.5)
Machine3 = Machine(3, 0.1)
Machine4 = Machine(4, 0.3)
Machine5 = Machine(5, 0.2)
Machine6 = Machine(6, 0.7)
Machine7 = Machine(7, 0.1)
Machine8 = Machine(8, 0.5)

Machines = [Machine1, Machine2, Machine3, Machine4, Machine5, Machine6, Machine7, Machine8]

class Event : 
    def __init__(self, time) :
        self.time = time 
        
class Affectation(Event):
    pass

class Liberation(Event):
    def __init__(self, time,  worker_num, machine_num, product): 
        self.time = time
        self.worker_num = worker_num
        self.machine_num = machine_num
        self.product = product

class Product_arrival(Event): 
    def __init__(self, time, num_prod):
        self.time = time
        self.number = num_prod


### Liste d'évenements  et de travailleurs disponibles
    
Events = []

Waiting_workers = []



def next_event(Events):
    next_event = Events.pop(0) # on récupère le prochain évènement
    
    if  isinstance(next_event, Product_arrival): 
        num_prod = next_event.number #on récupère le numéro du produit
        product = Products[num_prod - 1]
        num_machine = product.path[0] #on détermine la 1ere machine où doit passer le produit
        machine = Machines[num_machine -1]
        if not machine.queue == 0 : #on regarde si la liste est vide
            machine.queue.append(product)
            product.arrivals.append(next_event.time)
            print( str(next_event.time) + ' : ' + colored('Product ' + str(num_prod), 'green') +  ' arrives at' + colored(' Machine ' + str(num_machine), 'red') )
            return worker_affectation(next_event.time)  #on lance l'affectation d'employés
            
    if isinstance(next_event, Liberation): 
        #par la suite créer une fonction libération
        machine_num = next_event.machine_num
        machine = Machines[machine_num - 1] #faire fonction get_machine
        machine.occupation = 0 # on libère la machine
        print (str(next_event.time) + ' : ' + colored('Machine ' + str(machine_num), 'red') + ' is liberated by'  + colored(' Worker ' + str(next_event.worker_num), 'cyan' ))
        #on pourra songer à indiquer dans occupied le worker qui travaille sur la machine 0 (vide , 1 ,2,3,4  ), idem pour les machines
        if next_event.product.path.index(machine_num) +1 != len(next_event.product.path):# est ce que le produit doit passer par d'autres machines
            next_machine_number = next_event.product.path[ next_event.product.path.index(machine_num) + 1 ] #on identifie ou la machine actuelle se situe dans le chemin puis on détermine la prochaine 
            Machines[next_machine_number -1].queue.append(next_event.product) # on envoie le produit dans la file d'attente de la prochaine machine
            print( str(next_event.time) + ' : ' + colored('Product ' + str(next_event.product.number), 'green') +  ' is sent to' + colored(' Machine '+ str(next_machine_number), 'red')  ) 
        
        else : 
            print( str(next_event.time) + ' : ' + colored('Product ' + str(next_event.product.number), 'green') +  ' is finished'   ) 
            product = Products[next_event.product.number - 1]
            product.departures.append(next_event.time)
            
        Waiting_workers.append(Workers[next_event.worker_num - 1]) #on ajoute le travailleurs à la file de travailleurs libres
        
        
        return worker_affectation(next_event.time)
  

      
### Affectation basique : on affecte le premier qui marche       

def worker_affectation(time) :
    worker_index = 0
    for worker in Waiting_workers :  # on essaie d'affecter chacun des travailleurs de la file d'attente
        #On établit la liste des machines sur lesquels on peut travailler
        Machines_available = []
        for machine in Machines :
            if len(machine.queue) != 0 :
                if machine.occupation == 0 :
                    Machines_available.append(machine)
        for machine in Machines_available : 
            if worker.skills[machine.number - 1]==1: #on voit s'il peut travailler sur la machine
                Waiting_workers.pop(worker_index)
                machine.occupation = 1 
                product = machine.queue.pop(0) #on retire le produit de la file d'attente
                time_interval = product.duration[machine.number -1] #on récupère l'intervalle de temps que peut prendre le produit pour passer sur la machine
                exact_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1) #prends un entier dans l'intervalle
                Events.append(Liberation(time + exact_duration, worker.number, machine.number, product)) # on crée le nouvel évènement
                Events.sort(key=lambda x: x.time) #on trie selon le temps 
                print( str(time) + ' : ' + colored('Worker ' + str(worker.number), 'cyan' )+ ' is affected at' + colored(' Machine ' + str(machine.number), 'red'))
        worker_index+=1
            
### Affectation suivant l'heuristique

def worker_affectation_bis(time) : 
    worker_index = 0
    machine_index = 0
    for worker in Waiting_workers :
        Machines_available = []
        for machine in Machines :
            if len(machine.queue) != 0 :
                if machine.occupation == 0 :
                    if machine.index in worker.skills :
                        Machines_available.append(machine)
        if len(Machines_available) == 0 :
            worker_index += 1
        elif len(Machines_available) == 1 :
            machine = Machines_available[0]
            Waiting_workers.pop(worker_index)
            machine.occupation = 1
            product = machine.pop(0) #on retire le produit de la file d'attente
            time_interval = product.path[Machines.available[0].number] #on récupère l'intervalle de temps que peut prendre le produit pour passer sur la machine
            penibility = Machines[machine_index].penibility
            initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1) #prends un entier dans l'intervalle
            duration = initial_duration * ( 1 + delta * penibility * (math.log(1 + worker.fatigue) ))
            update_fatigue(worker,duration,penibility)
            Events.append(Liberation(time + duration, worker, machine, product)) # on crée le nouvel évènement
            worker_index +=1
        else : 
            # On construit dans un premier temps la matrice A
            A = np.zeros((len(Machines_available),2))
            for i in range(len(Machines_available)) :
                #Critère C1 : SPT
                time_interval = product.path[Machines_available[i].number]
                initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1)
                penibility = Machines_available[i].penibility
                duration = initial_duration * ( 1 + delta * penibility * (math.log(1 + worker.fatigue) ))
                A[i][0] = duration
                #Critère C2 : LNQ 
                queue = Machines_available[i].queue
                lower_bound_fatigue = worker.fatigue
                duration = 0
                for j in range(len(queue)) : 
                    product_queued = queue[j]
                    time_interval = product_queued.path[Machines_available[i].number]
                    initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1)
                    duration = duration + initial_duration * ( 1 + delta * penibility * (math.log(1 + lower_bound_fatigue) ))
                A[i][1] = duration
                
            # On normalise cette matrice
            #... Affaire à suivre
                        
 ##Créer une fonction pour la fatigue               
        
def update_fatigue(worker,duration, penibility):
    fatigue = worker.fatigue
    new_fatigue_level = fatigue + (1 - fatigue) * (1 - math.exp(-penibility*duration))
    worker.increase_fatigue(new_fatigue_level)
    
 ## Création d'une borne inférieure sur le niveau de fatigue

        
#worker affectation doit renvoyer un evenment liberation avec le worker et ma machine
def MFT() : 
    MFT = []
    for product in Products :
        total = 0 
        for i  in range(len(product.departures)) : # on parcourt departures car certains produits peuvent encore être dans le système
            total += product.departures[i] - product.arrivals[i]
        MFT.append(total)
    return MFT
  
def generate_items_arrival():
    time = 0 
    
 
 #Test : 
Waiting_workers = [Worker1, Worker2, Worker3, Worker4]
Events.append(Product_arrival(0,1))
next_event(Events)
next_event(Events)
next_event(Events)
next_event(Events)
next_event(Events)
next_event(Events)
MFT = MFT()
print(MFT)