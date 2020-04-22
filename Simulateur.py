# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:30:22 2020
@author: louis
"""
import random 
import math
from termcolor import colored
import parameters as param
from productArrival import product_arrival
from topsis import topsis
from objet import Product, Worker, Machine, Liberation, Product_arrival

#Paramètre représentant l'influence de la fatigue
delta = param.delta

#Importance accordée à chacun des deux critères
nu = param.nu

#Cas d'étude
cas = param.nb_case

#On crée les listes d'objet : produits, ouvriers et machines
Products = []
for i in range(1,5):
    Products.append(Product(i, param.path[i-1], param.duration[i-1]))
    
Workers = []
for i in range(1,5):
    Workers.append(Worker(i, param.skill_matrix[cas-1][i-1]))
    
Machines = []
for i in range(1,9):
    Machines.append(Machine(i, param.penibility[i-1]))


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
            time_interval = product.duration[num_machine - 1]
            initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1)
            Machines[num_machine - 1].time_queue.append(initial_duration)
            return heuristique(next_event.time)  #on lance l'affectation d'employés
        else : 
            machine.queue.append(product)
            product.arrivals.append(next_event.time)
            print( str(next_event.time) + ' : ' + colored('Product ' + str(num_prod), 'green') +  ' arrives at' + colored(' Machine ' + str(num_machine), 'red') )
            
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
            time_interval = next_event.product.duration[next_machine_number - 1]
            initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1)
            Machines[next_machine_number -1].time_queue.append(initial_duration)
            print( str(next_event.time) + ' : ' + colored('Product ' + str(next_event.product.number), 'green') +  ' is sent to' + colored(' Machine '+ str(next_machine_number), 'red')  ) 
        
        else : 
            print( str(next_event.time) + ' : ' + colored('Product ' + str(next_event.product.number), 'green') +  ' is finished'   ) 
            product = Products[next_event.product.number - 1]
            product.departures.append(next_event.time)
            
        Waiting_workers.append(Workers[next_event.worker_num - 1]) #on ajoute le travailleurs à la file de travailleurs libres
        
        
        return heuristique(next_event.time)
  

def basic(time) :
    worker_index = 0
    copy_waiting_workers = []
    for i in range(len(Waiting_workers)) :
        copy_waiting_workers.append(Waiting_workers[i])
    for worker in copy_waiting_workers :  # on essaie d'affecter chacun des travailleurs de la file d'attente
        #On établit la liste des machines sur lesquels on peut travailler
        affected = False
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
                affected = True
                break
        if not affected : 
            worker_index+=1

# Affectation selon l'heuristique définie
def heuristique(time) : 
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
            affectation(machine, worker, worker_index, time)
            
        #Troisième cas : au moins deux machines sont disponibles, utilisation de l'heuristique
        else : 
            
            """Ici, on peut utiliser n'importe quelle heuristique en remplaçant
            la fonction topsis par une autre heuristique"""
            #On appelle topsis
            machine = Machines_available[topsis(Machines_available, worker)]
            
            #Affectation
            affectation(machine, worker, worker_index, time)
         
            
#Permet d'affecter un worker à une machine
def affectation(machine, worker, worker_index, time) :
    Waiting_workers.pop(worker_index)
    machine.occupation = 1
    product = machine.queue.pop(0) #on retire le produit de la file d'attente
    #time_interval = product.duration[machine.number - 1] #on récupère l'intervalle de temps que peut prendre le produit pour passer sur la machine
    penibility = machine.penibility
    initial_duration = machine.time_queue.pop(0) #prends un entier dans l'intervalle
    exact_duration = initial_duration * ( 1 + delta * penibility * (math.log(1 + worker.fatigue) ))
    update_fatigue(worker, exact_duration, penibility)
    Events.append(Liberation(time + exact_duration, worker.number, machine.number, product)) # on crée le nouvel évènement
    Events.sort(key=lambda x: x.time) #on trie selon le temps
    print( str(time) + ' : ' + 'Worker ' + str(worker.number) + ' is affected at machine ' + str(machine.number))


#Fonction actualisant le niveau de fatigue après calcul                       
def update_fatigue(worker,duration, penibility):
    fatigue = worker.fatigue
    new_fatigue_level = fatigue + (1 - fatigue) * (1 - math.exp(-penibility*duration))
    worker.increase_fatigue(new_fatigue_level)
        
#Calcul du mean flowtime
def MFT() : 
    MFT = []
    for product in Products :
        total = 0 
        for i  in range(len(product.departures)) : # on parcourt departures car certains produits peuvent encore être dans le système
            total += product.departures[i] - product.arrivals[i]
        MFT.append(total)
    return MFT

#Fonction permettant de dépiler les événements    
def run(Events): 
    while len(Events) != 0 :
        next_event(Events)

#Test : 

#Waiting_workers = [Workers[i] for i in range(len(Workers))]
#
#Events.append(Product_arrival(0,1))
#Events.append(Product_arrival(0,2))
#Events.append(Product_arrival(0,3))
#Events.append(Product_arrival(0,4))
#Events.append(Product_arrival(10,1))
#run(Events)
#MFT = MFT()
#print(MFT)

#Journée de 8h

Waiting_workers = [Workers[i] for i in range(len(Workers))]

def average_day() : 
    #Génération de la totalité des arrivées de produits
    for i in range(4) : 
        product_i = product_arrival[i]
        for j in range (len(product_i)) : 
            Events.append(Product_arrival(product_i[j],i+1))
    Events.sort(key=lambda x: x.time) #on trie selon le temps 
    
    #On traite les événements
    run(Events)
    Average_MFT = MFT()
    print(Average_MFT)
    