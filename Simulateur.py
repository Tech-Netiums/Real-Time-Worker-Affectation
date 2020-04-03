# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:30:22 2020

@author: louis
"""

class Produit : 
    def __init__(self, path, duration):
        self.path = path 
        self.duration = duration 
        
        
Produit1 = Produit([1,2,3,4,8], [[14,17], [5,8], [28,32], [2,4], None, None, None, [30,37]])
Produit2 = Produit([2,4,7], [None, [10,13], None, [20,25], None, None, [6,8], None ])
Produit3 = Produit([3,5,1], [[25,28], None, [5,10], None, [10,14], None, None, None])
Produit4= Produit([5,6,7,8], [None, None, None, None, [5,9], [12,15], [30,34], [3,7]])
        
class Worker :
    def __init__(self, Skills): 
        self.skills = Skills
        self.fatigue = 0
        
    def increase_fatigue(self, new_fatigue_level): 
        self.fatigue = new_fatigue_level
    
Worker1 = Worker([1, 1, 0, 0, 0, 0, 0, 0])
Worker2 = Worker([0, 0, 1, 1, 0, 0, 0, 0])
Worker3 = Worker([0, 0, 0, 0, 1, 1, 0, 0])
Worker4 = Worker([0, 0, 0, 0, 0, 0, 1, 1])


class Machine : 
    def __init__(self, number, penibility):
        self.number = number
        self.queue = []
        
Machine1 = Machine(1, 0.8)
Machine2 = Machine(2, 0.5)
Machine3 = Machine(3, 0.1)
Machine4 = Machine(4, 0.3)
Machine5 = Machine(5, 0.2)
Machine6 = Machine(6, 0.7)
Machine7 = Machine(7, 0.1)
Machine8 = Machine(8, 0.5)


