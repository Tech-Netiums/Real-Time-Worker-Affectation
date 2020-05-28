# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:30:22 2020
@author: louis
"""
import random 
import math
import numpy as np
from termcolor import colored
import matplotlib.pyplot as plt
import parameters as param
from productArrival import product_arrival, product_arrival_n_days
from topsis import topsis, SPT, loulou
from objet import Product, Worker, Machine, Liberation, Product_arrival
from fatigueMeunier import fatigueMeunier, deuxmachines
from heuristiqueSimon import heuristique_simon1
from progdynamique import prog_dynamique

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


def next_event(Events,weight):
    next_event = Events.pop(0) # on récupère le prochain évènement
    
    if  isinstance(next_event, Product_arrival): 
        num_prod = next_event.number #on récupère le numéro du produit
        product = Products[num_prod - 1]
        num_machine = product.path[0] #on détermine la 1ere machine où doit passer le produit
        machine = Machines[num_machine -1]
        time_interval = product.duration[num_machine - 1]
        initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1)
        machine.time_queue.append(initial_duration)
        if len(machine.queue) == 0 : #on regarde si la liste est vide
            machine.queue.append(product)
            product.arrivals.append(next_event.time)
            #print( str(next_event.time) + ' : ' + colored('Product ' + str(num_prod), 'green') +  ' arrives at' + colored(' Machine ' + str(num_machine), 'red') )
            return heuristique(next_event.time, weight)  #on lance l'affectation d'employés
        else : 
            machine.queue.append(product)
            product.arrivals.append(next_event.time)
            #print( str(next_event.time) + ' : ' + colored('Product ' + str(num_prod), 'green') +  ' arrives at' + colored(' Machine ' + str(num_machine), 'red') )
            
    if isinstance(next_event, Liberation): 
        #par la suite créer une fonction libération
        machine_num = next_event.machine_num
        machine = Machines[machine_num - 1] #faire fonction get_machine
        machine.occupation = 0 # on libère la machine
        #print (str(next_event.time) + ' : ' + colored('Machine ' + str(machine_num), 'red') + ' is liberated by'  + colored(' Worker ' + str(next_event.worker_num), 'cyan' ))
        #on pourra songer à indiquer dans occupied le worker qui travaille sur la machine 0 (vide , 1 ,2,3,4  ), idem pour les machines
        if next_event.product.path.index(machine_num) +1 != len(next_event.product.path):# est ce que le produit doit passer par d'autres machines
            next_machine_number = next_event.product.path[ next_event.product.path.index(machine_num) + 1 ] #on identifie ou la machine actuelle se situe dans le chemin puis on détermine la prochaine 
            Machines[next_machine_number -1].queue.append(next_event.product) # on envoie le produit dans la file d'attente de la prochaine machine
            time_interval = next_event.product.duration[next_machine_number - 1] #on récupèere l'intervalle de temps du process
            initial_duration = random.randrange(time_interval[0],time_interval[1]+1 , 1)  #on genere le temps de process du porduit
            Machines[next_machine_number -1].time_queue.append(initial_duration)
            #print( str(next_event.time) + ' : ' + colored('Product ' + str(next_event.product.number), 'green') +  ' is sent to' + colored(' Machine '+ str(next_machine_number), 'red')  ) 
        
        else : 
            #print( str(next_event.time) + ' : ' + colored('Product ' + str(next_event.product.number), 'green') +  ' is finished'   ) 
            product = Products[next_event.product.number - 1]
            product.departures.append(next_event.time)
            
        Waiting_workers.append(Workers[next_event.worker_num - 1]) #on ajoute le travailleurs à la file de travailleurs libres
        
        
        return heuristique(next_event.time, weight)
  
def random_affectation(Machines_available, worker) :
    return random.randrange(0,len(Machines_available),1)

# Affectation selon l'heuristique définie
def heuristique(time, weight = nu) : 
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
            machine = Machines_available[heuristique_simon1(Machines_available, worker, Workers)]
            
            #Affectation
            affectation(machine, worker, worker_index, time)
         
            
#Permet d'affecter un worker à une machine
def affectation(machine, worker, worker_index, time) :
    Waiting_workers.pop(worker_index)
    machine.occupation = 1
    product = machine.queue.pop(0) #on retire le produit de la file d'attente
    #time_interval = product.duration[machine.number - 1] #on récupère l'intervalle de temps que peut prendre le produit pour passer sur la machine
    penibility = machine.penibility
    initial_duration = machine.time_queue.pop(0) #récupere le temps inital depuis la file d'attente
    exact_duration = initial_duration * ( 1 + delta * (math.log(1 + worker.fatigue) ))
    update_fatigue(worker, exact_duration, penibility,time)
    Events.append(Liberation(time + exact_duration, worker.number, machine.number, product)) # on crée le nouvel évènement
    Events.sort(key=lambda x: x.time) #on trie selon le temps
    #print( str(time) + ' : ' + 'Worker ' + str(worker.number) + ' is affected at machine ' + str(machine.number))


#Fonction actualisant le niveau de fatigue après calcul                       
def update_fatigue(worker,duration, penibility,time):
    fatigue = worker.fatigue
    new_fatigue_level = fatigue + ((1 - fatigue) * (1 - math.exp(-penibility*duration)))/5
    worker.increase_fatigue(new_fatigue_level,time)
        
#Calcul du mean flowtime
def MFT() : 
    MFT = []
    for product in Products :
        total = 0 
        lenght = len(product.departures)
        for i  in range(lenght) : 
            # on parcourt departures car certains produits peuvent encore être dans le système
            departure = product.departures.pop(0)
            arrival = product.arrivals.pop(0)
            total += departure - arrival
        MFT.append(total)
    sum_MFT = 0
    for i in range(4) : 
        sum_MFT += MFT[i]
    return sum_MFT

#Fonction permettant de dépiler les événements    
def run(Events, weight): 
    time_out = 0
    while len(Events) != 0 :
        next_event(Events, weight)
        if len(Events) == 1 :
            time_out = Events[0].time
    return time_out
    
        
#Fonction permettant de tracer les courbes d'évolution de la fatigue des workers
def plot_fatigue() :
    for i in range(len(Workers)) :
        plt.plot(Workers[i].list_time,Workers[i].list_fatigue, label = "Worker" + str(i+1)) 
        plt.legend()
        #print(Workers[i].list_time,Workers[i].list_fatigue)
    plt.xlabel("Time")
    plt.ylabel("Level of fatigue")

#Journée de 8h

Waiting_workers = [Workers[i] for i in range(len(Workers))]

def average_day(prod_arrival, weight) : 
    #Génération de la totalité des arrivées de produits
    for i in range(4) : 
        product_i = prod_arrival[i]
        for j in range (len(product_i)) : 
            Events.append(Product_arrival(product_i[j],i+1))
    Events.sort(key=lambda x: x.time) #on trie selon le temps
    #On traite les événements
    time = run(Events, weight)
    mft = MFT()
    return mft, time


#Simuler n journées de 8h

def simulation_n_days(weight) : 
    MFTs = []
    average_mft = 0
    variance = 0
    time = 0
    #Calcul de la moyenne 
    for i in range(param.number_of_days) :
        day_i, time_i= average_day(product_arrival_n_days[i], weight)
        average_mft += day_i
        time += time_i
        MFTs.append(day_i)
    average_mft = average_mft/param.number_of_days
    average_time = time/param.number_of_days
    #Calcul de la variance
    for i in range(param.number_of_days) :
        #Au début de chaque journée les ouvriers n'ont aucune fatigue
        for j in range(len(Workers)):
            Workers[j].fatigue = 0
        variance += (MFTs[i] - average_mft)**2
    standard_deviation = math.sqrt(variance/param.number_of_days)
    #plot_bar(MFTs,average_mft)
    return average_mft,standard_deviation, average_time

def plot_bar(MFTs,average_mft) :
    interval = int((average_mft*0.1)//10*10)
    MFT_max = max(MFTs)
    number_of_interval = int(MFT_max//interval) +1
    freq = [0 for i in range(number_of_interval)]
    for i in range(len(MFTs)) :
        place = int(MFTs[i]//interval)
        freq[place] += 1
    x = [i*interval for i in range(number_of_interval)]
    plt.bar(x,freq, width = interval*3/4)   
    plt.xlabel("MFT")
    plt.ylabel("frequency")

nu_1 = np.linspace(0,1,101)
nu_list = [[nu_1[i],1-nu_1[i]] for i in range(100)]

def best_coeff(nu_list) :
    nu_opt = nu_list[0]
    MFT_opt = simulation_n_days(nu_list[0])[0]
    for i in range(1,len(nu_list)) :
        if simulation_n_days(nu_list[i])[0] < MFT_opt :
            MFT_opt = simulation_n_days(nu_list[i])[0]
            nu_opt = nu_list[i]
    return nu_opt