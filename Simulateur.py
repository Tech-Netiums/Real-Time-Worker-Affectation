# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:30:22 2020

@author: louis
"""
import random 
import math
import numpy as np
import parameters as param

#Paramètre représentant l'influence de la fatigue
delta = param.delta

#Importance accordée à chacun des deux critères
nu = param.nu

#Cas d'étude
cas = param.nb_case

#Création des 4 types de produits
class Product : 
    def __init__(self, number, path, duration):
        self.number = number
        self.path = path 
        self.duration = duration 
        
Products = []
for i in range(1,5):
    Products.append(Product(i, param.path[i-1], param.duration[i-1]))

#Création des 4 travailleurs
class Worker :
    def __init__(self, number,  Skills): 
        self.number = number 
        self.skills = Skills
        self.fatigue = 0
        
    def increase_fatigue(self, new_fatigue_level): 
        self.fatigue = new_fatigue_level
    
Workers = []
for i in range(1,5):
    Workers.append(Worker(i, param.skill_matrix[cas-1][i-1]))

#Création des 8 machines
class Machine : 
    def __init__(self, number, penibility):
        self.number = number
        self.queue = []
        self.occupation = 0
        self.penibility = penibility
        
Machines = []
for i in range(1,9):
    Machines.append(Machine(i, param.penibility[i-1]))

#Création des types d'évènements
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
    try:
        next_event = Events.pop(0) # on récupère le prochain évènement
        
        if  isinstance(next_event, Product_arrival): 
            num_prod = next_event.number #on récupère le numéro du produit
            product = Products[num_prod - 1]
            num_machine = product.path[0] #on détermine la 1ere machine où doit passer le produit
            machine = Machines[num_machine -1]
            if not machine.queue == 0 : #on regarde si la liste est vide
                machine.queue.append(product)
                print( str(next_event.time) + ' : ' + 'Product ' + str(num_prod) +  ' arrives at machine ' + str(num_machine) )
                return worker_affectation_bis(next_event.time)  #on lance l'affectation d'employés
                
        if isinstance(next_event, Liberation): 
            #par la suite créer une fonction libération
            machine_num = next_event.machine_num
            machine = Machines[machine_num - 1] #faire fonction get_machine
            machine.occupation = 0 # on libère la machine
            print (str(next_event.time) + ' : ' + 'Machine ' + str(machine_num) + ' is liberated by worker ' + str(next_event.worker_num))
            #on pourra songer à indiquer dans occupied le worker qui travaille sur la machine 0 (vide , 1 ,2,3,4  ), idem pour les machines
            if next_event.product.path.index(machine_num) +1 != len(next_event.product.path):# est ce que le produit doit passer par d'autres machines
                next_machine_number = next_event.product.path[ next_event.product.path.index(machine_num) + 1 ] #on identifie ou la machine actuelle se situe dans le chemin puis on détermine la prochaine 
                Machines[next_machine_number -1].queue.append(next_event.product) # on envoie le produit dans la file d'attente de la prochaine machine
                print( str(next_event.time) + ' : ' + 'Product ' + str(next_event.product.number) +  ' is sent to machine ' + str(next_machine_number) ) 
            
            Waiting_workers.append(Workers[next_event.worker_num - 1]) #on ajoute le travailleurs à la file de travailleurs libres
            
            
            return worker_affectation_bis(next_event.time)
    except:
        pass
  

      
### Affectation basique : on affecte le premier qui marche       

def worker_affectation(time) :
    #On crée une copie de la liste des workers
    worker_index = 0
    copy_waiting_worker = []
    for i in range(len(Waiting_workers)) :
        copy_waiting_worker.append(Waiting_workers[i])
    for worker in copy_waiting_worker :  # on essaie d'affecter chacun des travailleurs de la file d'attente
        #On établit la liste des machines sur lesquels on peut travailler
        affected = False
        Machines_available = []
        for machine in Machines :
            if len(machine.queue) != 0 :
                if machine.occupation == 0 :
                    Machines_available.append(machine)
        for machine in Machines_available : 
            if worker.skills[machine.number - 1] == 1: #on voit s'il peut travailler sur la machine
                Waiting_workers.pop(worker_index)
                machine.occupation = 1 
                product = machine.queue.pop(0) #on retire le produit de la file d'attente
                time_interval = product.duration[machine.number -1] #on récupère l'intervalle de temps que peut prendre le produit pour passer sur la machine
                exact_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1) #prends un entier dans l'intervalle
                Events.append(Liberation(time + exact_duration, worker.number, machine.number, product)) # on crée le nouvel évènement
                Events.sort(key=lambda x: x.time) #on trie selon le temps 
                print( str(time) + ' : ' + 'Worker ' + str(worker.number) + ' is affected at machine ' + str(machine.number))
                affected = True
                break
        if not affected :
            worker_index += 1
            
### Affectation suivant l'heuristique

def worker_affectation_bis(time) : 
    worker_index = 0
    copy_waiting_worker = []
    for i in range(len(Waiting_workers)) :
        copy_waiting_worker.append(Waiting_workers[i])
    for worker in copy_waiting_worker :
        Machines_available = []
        for machine in Machines :
            if len(machine.queue) != 0 :
                if machine.occupation == 0 :
                    if worker.skills[machine.number - 1] == 1:
                        Machines_available.append(machine)
                                
        #Premier cas : pas de machines dispo, le worker doit attendre
        if len(Machines_available) == 0 :
            worker_index += 1
            
        #Second cas : une seule machine disponible, on assigne le worker
        elif len(Machines_available) == 1 :
            machine = Machines_available[0]
            Waiting_workers.pop(worker_index)
            machine.occupation = 1
            product = machine.queue.pop(0) #on retire le produit de la file d'attente
            time_interval = product.duration[machine.number - 1] #on récupère l'intervalle de temps que peut prendre le produit pour passer sur la machine
            penibility = machine.penibility
            initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1) #prends un entier dans l'intervalle
            exact_duration = initial_duration * ( 1 + delta * penibility * (math.log(1 + worker.fatigue) ))
            update_fatigue(worker, exact_duration, penibility)
            Events.append(Liberation(time + exact_duration, worker.number, machine.number, product)) # on crée le nouvel évènement
            Events.sort(key=lambda x: x.time) #on trie selon le temps 
            print( str(time) + ' : ' + 'Worker ' + str(worker.number) + ' is affected at machine ' + str(machine.number))
            
        #Troisième cas : au moins deux machines sont disponibles, utilisation de l'heuristique
        else : 
            # On construit dans un premier temps la matrice A
            A = np.zeros((len(Machines_available),2))
            for i in range(len(Machines_available)) :
                machine = Machines_available[i]
                
                #Critère C1 : SPT
                time_interval = product.duration[machine.number - 1]
                initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1)
                penibility = machine.penibility
                exact_duration = initial_duration * ( 1 + delta * penibility * (math.log(1 + worker.fatigue) ))
                A[i][0] = exact_duration
                
                #Critère C2 : LNQ 
                queue = machine.queue
                lower_bound_fatigue = worker.fatigue
                exact_duration = 0
                for j in range(len(queue)) : 
                    product_queued = queue[j]
                    time_interval = product_queued.duration[machine.number - 1]
                    initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1)
                    exact_duration += initial_duration * ( 1 + delta * penibility * (math.log(1 + lower_bound_fatigue) ))
                A[i][1] = exact_duration
                
            # On normalise cette matrice 
            R = np.zeros((len(Machines_available),2))
            for j in range(2) :
                norm = 0
                for i in range(len(Machines_available)) :
                    norm +=  A[i][j]
                norm = math.sqrt(norm)
                for i in range(len(Machines_available)) :
                    R[i][j] = A[i][j]/norm
                    
            #On pondère la matrice
            V = np.zeros((len(Machines_available),2))
            for j in range(2) :
                for i in range(len(Machines_available)) :
                    V[i][j] = nu[j]*R[i][j]
            
            #Détermination de la pire et de la meilleure alternative
            min_C = [V[0][0], V[0][1]]
            max_C = [V[0][0], V[0][1]]
            for i in range(len(Machines_available)) :
                for j in range(2) :
                    if V[i][j] < min_C[j] :
                        min_C[j] = V[i][j]
                    elif V[i][j] < max_C[j] : 
                        max_C[j] = V[i][j]
                        
            #best solution
            IA = [max_C[1], min_C[0]]
            #worst solution
            WA = [max_C[0], min_C[1]]
            
            #Mesure de la distance euclidienne 
            IS = []
            WS = []
            for j in range(len(Machines_available)) : 
                ISj = math.sqrt(V[j][0] - IA[0] + V[j][1] - IA[1])
                WSj = math.sqrt(V[j][0] - WA[0] + V[j][1] - WA[1])
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
            machine = Machines_available[machine_index]
            
            #Affectation
            Waiting_workers.pop(worker_index)
            machine.occupation = 1
            product = machine.queue.pop(0) #on retire le produit de la file d'attente
            time_interval = product.duration[machine.number - 1] #on récupère l'intervalle de temps que peut prendre le produit pour passer sur la machine
            penibility = machine.penibility
            initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1) #prends un entier dans l'intervalle
            exact_duration = initial_duration * ( 1 + delta * penibility * (math.log(1 + worker.fatigue) ))
            update_fatigue(worker, exact_duration, penibility)
            Events.append(Liberation(time + exact_duration, worker.number, machine.number, product)) # on crée le nouvel évènement
            Events.sort(key=lambda x: x.time) #on trie selon le temps 
            print( str(time) + ' : ' + 'Worker ' + str(worker.number) + ' is affected at machine ' + str(machine.number))
    
                        
 ##Créer une fonction pour la fatigue               
        
def update_fatigue(worker,duration, penibility):
    fatigue = worker.fatigue
    new_fatigue_level = fatigue + (1 - fatigue) * (1 - math.exp(-penibility*duration))
    worker.increase_fatigue(new_fatigue_level)
    
 ## Création d'une borne inférieure sur le niveau de fatigue

        
#worker affectation doit renvoyer un evenment liberation avec le worker et ma machine
 
 
 

 
 #Test : 
Waiting_workers = Workers
Events.append(Product_arrival(0,1))
next_event(Events)
next_event(Events)
next_event(Events)
next_event(Events)
next_event(Events)
next_event(Events)
 
        
