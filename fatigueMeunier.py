# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:52:00 2020

@author: simon
"""

import math
import numpy as np
from parameters import delta
from objet import Worker, Machine

R = 5

def createlist(i,j,r,k,fatigue,d,s,t,pi,m,n) :
    L = []
    #On travaille sur l'indice j
    if k == 0 : 
        for rp in range(r+1) :
            if fatigue[i][j-1][rp] != None and fatigue[i][j-1][rp] + (1 - fatigue[i][j-1][rp])*(1 - math.exp(-d[1]*t[j-1])) <= r/R :
                L.append(rp)
                
        if L != [] :
            phi0 = phi(i,j,L[0],0,fatigue,d)
            Lmin = pi[i][j-1][L[0]] + (m+n+1-i-j)*t[j-1]*phi0
            index_Lmin = L[0]
            for rp in L :
                phirp = phi(i,j,rp,0,fatigue,d)
                if pi[i][j-1][rp] + (m+n+1-i-j)*t[j-1]*phirp < Lmin :
                    Lmin = pi[i][j-1][rp] + (m+n+1-i-j)*t[j-1]*phirp
                    index_Lmin = rp
            return index_Lmin
        else :
            return None
                
    #On travaille sur l'indice i
    if k == 1 :
        for rp in range(r+1) :
            if fatigue[i-1][j][rp] != None and fatigue[i-1][j][rp] + (1 - fatigue[i-1][j][rp])*(1 - math.exp(-d[0]*s[i-1])) <= r/R :
                L.append(rp)
        
        if L != [] :
            phi0 = phi(i,j,L[0],1,fatigue,d)
            Lmin = pi[i-1][j][L[0]] + (m+n+1-i-j)*s[i-1]*phi0
            index_Lmin = L[0]
            for rp in L :
                phirp = phi(i,j,rp,1,fatigue,d)
                if pi[i-1][j][rp] + (m+n+1-i-j)*s[i-1]*phirp < Lmin :
                    Lmin = pi[i-1][j][rp] + (m+n+1-i-j)*s[i-1]*phirp
                    index_Lmin = rp
            return index_Lmin
        else :
            return None
        
def affectation(i,j,r,k,r_min,pi,former_neighbour,fatigue,m,n,s,t,d) :
    #On travaille sur l'indice j
    if k == 0 :
        return pi[i][j-1][r_min] + (m+n+1-i-j)*t[j-1]*phi(i,j,r_min,0,fatigue,d),(i,j-1,r_min), fatigue[i][j-1][r_min] + (1 - fatigue[i][j-1][r_min])*(1 - math.exp(-d[1]*t[j-1]))     
    #On travaille sur l'indice i
    if k == 1 :
        return pi[i-1][j][r_min] + (m+n+1-i-j)*s[i-1]*phi(i,j,r_min,1,fatigue,d), (i-1,j,r_min), fatigue[i-1][j][r_min] + (1 - fatigue[i-1][j][r_min])*(1 - math.exp(-d[0]*s[i-1]))
        

def phi(i,j,r,k,fatigue,d) :
    #On travaille sur l'indice j
    if k == 0 :
        return 1 + delta * math.log(1 + fatigue[i][j-1][r])
    #On travaille sur l'indice i 
    if k==1 :
        return 1 + delta * math.log(1 + fatigue[i-1][j][r])    

#Modèle avec fatigue pour deux machines
def deuxmachines(Machines_available, worker) :
    s = Machines_available[0].time_queue
    t = Machines_available[1].time_queue
    d = [Machines_available[0].penibility, Machines_available[1].penibility]
    m = len(s)
    n = len(t) 
    fatigue_init = worker.fatigue
    pi = [[[None for i in range(R+1)] for j in range(n+1)] for k in range(m+1)]
    former_neighbour = [[[None for i in range(R+1)] for j in range(n+1)] for k in range(m+1)]
    fatigue = [[[None for i in range(R+1)] for j in range(n+1)] for k in range(m+1)]
    for i in range(m+1) :    
        for j in range(n+1) :
            for r in range(R+1) :
                if (i,j) == (0,0) and fatigue_init <= r :
                    pi[i][j][r] = 0
                    fatigue[i][j][r] = fatigue_init
                else :     
                    
                    if i==0 :
                        r_min = createlist(i,j,r,0,fatigue,d,s,t,pi,m,n)
                        if r_min != None :
                            pi[i][j][r], former_neighbour[i][j][r], fatigue[i][j][r] = affectation(i,j,r,0,r_min,pi,former_neighbour,fatigue,m,n,s,t,d)
                            
                    elif j == 0 :
                        r_min = createlist(i,j,r,1,fatigue,d,s,t,pi,m,n)
                        if r_min != None :
                            pi[i][j][r], former_neighbour[i][j][r], fatigue[i][j][r] = affectation(i,j,r,1,r_min,pi,former_neighbour,fatigue,m,n,s,t,d)
                            
                    else :

                        ri_min = createlist(i,j,r,1,fatigue,d,s,t,pi,m,n)
                        rj_min = createlist(i,j,r,0,fatigue,d,s,t,pi,m,n)
                             
                        if ri_min != None and rj_min != None :
                            Limin = pi[i-1][j][ri_min] + (m+n+1-i-j)*s[i-1]*phi(i,j,ri_min,1,fatigue,d)
                            Ljmin = pi[i][j-1][rj_min] + (m+n+1-i-j)*t[j-1]*phi(i,j,rj_min,0,fatigue,d)
                            
                            if Limin < Ljmin : 
                                pi[i][j][r], former_neighbour[i][j][r], fatigue[i][j][r] = affectation(i,j,r,1,ri_min,pi,former_neighbour,fatigue,m,n,s,t,d)
                            
                            else : 
                                pi[i][j][r], former_neighbour[i][j][r], fatigue[i][j][r] = affectation(i,j,r,0,rj_min,pi,former_neighbour,fatigue,m,n,s,t,d)
                                
                        else :
                            
                            if ri_min != None :
                                pi[i][j][r], former_neighbour[i][j][r], fatigue[i][j][r] = affectation(i,j,r,1,ri_min,pi,former_neighbour,fatigue,m,n,s,t,d)
                            
                            if rj_min != None :
                                pi[i][j][r], former_neighbour[i][j][r], fatigue[i][j][r] = affectation(i,j,r,0,rj_min,pi,former_neighbour,fatigue,m,n,s,t,d)
                        
                                
    #On reconstruit le chemin                    
    path = []
    k = m
    l = n
    o = R
    target = former_neighbour[k][l][o]
    path.append((target[0],target[1]))
    while (target[0],target[1]) != (0,0) :
        k = target[0]
        l = target[1]
        o = target[2]
        target = former_neighbour[k][l][o]
        path.append((target[0],target[1]))
    
    path.reverse()
    if path[1] == (1,0) :
        print(0)
        return 0
    else :
        print(1)
        return 1 
    
#Modèle avec fatigue pour n machines
def fatigueMeunier(Machines_available, worker) :
    machines = []
    for i in range(len(Machines_available)) :
        machines.append(Machines_available[i])
    number_of_pairs = len(machines)//2
    alone_machine = len(machines)%2
    while number_of_pairs != 0 :
        nb_duel = 0
        winners = []
        for i in range(number_of_pairs) :
            nb_duel += 1
            print(nb_duel)
            duel = [machines[i],machines[i+1]]
            index = deuxmachines(duel,worker)
            winners.append(duel[index])
            if index == 0 :
                machines.pop(i+1)
            else :
                machines.pop(i)
        if alone_machine == 1 :
            winners.append(machines[-1])   
        number_of_pairs = len(machines)//2
        alone_machine = len(machines)%2
    for i in range(len(Machines_available)) : 
        if machines[0] == Machines_available[i] :
            print(i)
            return i
            