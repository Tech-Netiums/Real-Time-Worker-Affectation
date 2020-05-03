# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:08:02 2020

@author: simon
"""

#Classe des produits
class Product : 
    def __init__(self, number, path, duration):
        self.number = number
        self.path = path 
        self.duration = duration 
        self.arrivals = []
        self.departures = []

#Classe des travailleurs
class Worker :
    def __init__(self, number,  Skills): 
        self.number = number 
        self.skills = Skills
        self.fatigue = 0
        self.list_fatigue = [0]
        self.list_time = [0]
        
    def increase_fatigue(self, new_fatigue_level, time): 
        self.fatigue = new_fatigue_level
        self.list_fatigue.append(new_fatigue_level)
        self.list_time.append(time)
        
#Classe des machines
class Machine : 
    def __init__(self, number, penibility):
        self.number = number
        self.queue = []
        self.time_queue = []
        self.occupation = 0
        self.penibility = penibility

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