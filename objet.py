# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:08:02 2020

@author: simon
"""

class Product : 
    def __init__(self, number, path, duration):
        self.number = number
        self.path = path 
        self.duration = duration 
        self.arrivals = []
        self.departures = []

#Création des 4 travailleurs
class Worker :
    def __init__(self, number,  Skills): 
        self.number = number 
        self.skills = Skills
        self.fatigue = 0
        
    def increase_fatigue(self, new_fatigue_level): 
        self.fatigue = new_fatigue_level
        
#Création des 8 machines
class Machine : 
    def __init__(self, number, penibility):
        self.number = number
        self.queue = []
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