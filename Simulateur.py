# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:30:22 2020

@author: louis
"""
import random 


class Product : 
    def __init__(self, number, path, duration):
        self.number = number
        self.path = path 
        self.duration = duration 
        
        
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


### Liste d'évenements  et de travailleurs dispoonibles
    
Events = []

Waiting_workers = []



def next_event(Events):
    next_event = Events.pop(0) # on récupère le prochain évènement
    
    if  isinstance(next_event, Product_arrival): 
        num_prod = Product_arrival.number #on récupère le numéro du produit
        product = Products[num_prod - 1]
        num_machine = product.path[0] #on détermine la 1ere machine où doit passer le produit
        machine = Machines[num_machine -1]
        if not machine.queue : #on regarde si la liste est vide
            machine.queue.append(product)
            return worker_affectation(next_event.time)  #on lance l'affectation d'employés
            
    if isinstance(next_event, Liberation): 
        #par la suite créer une fonction libération
        machine_num = next_event.machine_num
        machine = Machines[machine_num -1] #faire fonction get_machine
        machine.occupied = 0 # on libère la machine
        #on pourra songer à indiquer dans occupied le worker qui travaille sur la machine 0 (vide , 1 ,2,3,4  ), idem pour les machines
        
        if next_event.product.path.index(machine_num) != len(next.event.product.path): # est ce que le produit doit passer par d'autres machines
         next_machine_number = next_event.product.path[ next_event.product.path.index(machine_num) + 1 ] #on identifie ou la machine actuelle se situe dans le chemin puis on détermine la prochaine 
         Machines[next_machine_number -1].queue.append(next_event.product) # on envoie le produit dans la file d'attente de la prochaine machine
        
        Waiting_workers.append(Workers[next_event.worker_num - 1]) #on ajoute le travailleurs à la file de travailleurs libres
        return worker_affectation(next_event.time)
  

      
### Affectation basique : on affecte le premier qui marche       

def worker_affectation(time) :
    worker_index = 0
    machine_index = 0
    for worker in Waiting_workers:  # on essaie d'affecter chacun des travailleurs de la file d'attente
        for machine in Machines : 
            if worker.skills[machine_index]==1: #on voit s'il peut travailler sur la machine
                Waiting_workers.pop(worker_index)
                machine.occupied = 1 
                product = machine.pop(0) #on retire le produit de la file d'attente
                time_interval = product.path[machine_index] #on récupère l'intervalle de temps que peut prendre le produit pour passer sur la machine
                duration = random.randrange(time_interval[0],time_interval[1]+1 , 1) #prends un entier dans l'intervalle
                Events.append(Liberation(time + duration, worker, machine, product)) # on crée le nouvel évènement
                machine_index +=1
            worker_index+=1
                
 ##Créer une fonction pour la fatigue               
        
        
        
#worker affectation doit renvoyer un evenment liberation avec le worker et ma machine
        