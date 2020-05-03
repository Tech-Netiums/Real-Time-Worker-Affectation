# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:52:00 2020

@author: simon
"""

import math
import numpy as np
from parameters import delta
from objet import Worker, Machine

R = 2

def createlist(i,j,r,k,fatigue,d,s,t) :
    L = []
    #On travaille sur l'indice j
    if k == 0 : 
        for rp in range(r+1) :
            if fatigue[i][j-1][rp] != None and fatigue[i][j-1][rp] + (1 - fatigue[i][j-1][rp])*(1 - math.exp(-d[1]*t[j-1])) <= r/R :
                L.append(rp)
    #On travaille sur l'indice i
    if k == 1 :
        for rp in range(r+1) :
            if fatigue[i-1][j][rp] != None and fatigue[i-1][j][rp] + (1 - fatigue[i-1][j][rp])*(1 - math.exp(-d[0]*s[i-1])) <= r/R :
                L.append(rp)
    return L

def phi(i,j,r,k,fatigue,d) :
    #On travaille sur l'indice j
    if k == 0:
        return 1 + delta * d[1] * math.log(1 + fatigue[i][j-1][r])
    #On travaille sur l'indice i 
    if k==1 :
        return 1 + delta * d[0] * math.log(1 + fatigue[i-1][j][r])    

#Modèle avec fatigue pour deux machines
def deuxmachines(Machines_available, worker) :
    s = Machines_available[0].time_queue
    t = Machines_available[1].time_queue
    d = [Machines_available[0].penibility, Machines_available[1].penibility]
    print(s,t,d)
    m = len(s)
    n = len(t) 
    pi = [[[None for i in range(R+1)] for j in range(n+1)] for k in range(m+1)]
    former_neighbour = [[[None for i in range(R+1)] for j in range(n+1)] for k in range(m+1)]
    fatigue = [[[None for i in range(R+1)] for j in range(n+1)] for k in range(m+1)]
    
    for i in range(m+1) :    
        for j in range(n+1) :
            for r in range(R+1) :
                if (i,j) == (0,0) :
                    pi[i][j][r] = 0
                    fatigue[i][j][r] = 0
                else :     
                    if i==0 :
                        L = createlist(i,j,r,0,fatigue,d,s,t)
                        if L != [] :
                            phi0 = phi(i,j,L[0],0,fatigue,d)
                            Lmin = pi[i][j-1][L[0]] + (m+n+1-i-j)*t[j-1]*phi0
                            index_Lmin = L[0]
                            for rp in L :
                                phirp = phi(i,j,rp,0,fatigue,d)
                                if pi[i][j-1][rp] + (m+n+1-i-j)*t[j-1]*phirp < Lmin :
                                    Lmin = pi[i][j-1][rp] + (m+n+1-i-j)*t[j-1]*phirp
                                    index_Lmin = rp  
                            pi[i][j][r] = pi[i][j-1][index_Lmin] + (m+n+1-i-j)*t[j-1]*phirp
                            former_neighbour[i][j][r] = (i,j-1,index_Lmin)
                            fatigue[i][j][r] = fatigue[i][j-1][index_Lmin] + (1 - fatigue[i][j-1][index_Lmin])*(1 - math.exp(-d[1]*t[j-1]))
                        
                    elif j == 0 :
                        L = createlist(i,j,r,1,fatigue,d,s,t)
                        if L != [] :
                            phi0 = phi(i,j,L[0],1,fatigue,d)
                            Lmin = pi[i-1][j][L[0]] + (m+n+1-i-j)*s[i-1]*phi0
                            index_Lmin = L[0]
                            for rp in L :
                                phirp = phi(i,j,rp,1,fatigue,d)
                                if pi[i-1][j][rp] + (m+n+1-i-j)*s[i-1]*phirp < Lmin :
                                    Lmin = pi[i-1][j][rp] + (m+n+1-i-j)*s[i-1]*phirp
                                    index_Lmin = rp  
                            pi[i][j][r] = pi[i-1][j][index_Lmin] + (m+n+1-i-j)*s[i-1]*phirp
                            former_neighbour[i][j][r] = (i-1,j,index_Lmin)
                            fatigue[i][j][r] = fatigue[i-1][j][index_Lmin] + (1 - fatigue[i-1][j][index_Lmin])*(1 - math.exp(-d[0]*s[i-1]))
                    
                    else :
                        
                        Li = createlist(i,j,r,1,fatigue,d,s,t)
                        Lj = createlist(i,j,r,0,fatigue,d,s,t)
                        Limin = np.inf
                        Ljmin = np.inf
                        index_Limin = None
                        index_Ljmin = None
                        
                        if Li != [] : 
                            phi0 = phi(i,j,Li[0],1,fatigue,d)
                            Limin = pi[i-1][j][Li[0]] + (m+n+1-i-j)*s[i-1]*phi0
                            index_Limin = Li[0]
                            for rp in Li :
                                phirp = phi(i,j,rp,1,fatigue,d)
                                if pi[i-1][j][rp] + (m+n+1-i-j)*s[i-1]*phirp < Limin :
                                    Limin = pi[i-1][j][rp] + (m+n+1-i-j)*s[i-1]*phirp
                                    index_Limin = rp  
                        
                        if Lj != [] :
                            phi0 = phi(i,j,Lj[0],0,fatigue,d)
                            Ljmin = pi[i][j-1][Li[0]] + (m+n+1-i-j)*t[j-1]*phi0
                            index_Ljmin = Lj[0]
                            for rp in Lj :
                                phirp = phi(i,j,rp,0,fatigue,d)
                                if pi[i][j-1][rp] + (m+n+1-i-j)*t[j-1]*phirp < Ljmin :
                                    Ljmin = pi[i][j-1][rp] + (m+n+1-i-j)*t[j-1]*phirp
                                    index_Ljmin = rp
                             
                        if Limin != np.inf and Ljmin != np.inf :
                            
                            if Limin < Ljmin : 
                                pi[i][j][r] = Limin
                                former_neighbour[i][j][r] = (i-1,j,index_Limin)
                                fatigue[i][j][r] = fatigue[i-1][j][index_Limin] + (1 - fatigue[i-1][j][index_Limin])*(1 - math.exp(-d[0]*s[i-1]))
                            
                            else : 
                                pi[i][j][r] = Ljmin
                                former_neighbour[i][j][r] = (i,j-1,index_Ljmin)
                                fatigue[i][j][r] = fatigue[i][j-1][index_Ljmin] + (1 - fatigue[i][j-1][index_Ljmin])*(1 - math.exp(-d[1]*t[j-1]))
                                
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
        return 0
    else :
        return 1 
    
#Modèle avec fatigue pour n machines
def fatigueMeunier(Machines_available, worker) :
    machines = []
    for i in range(len(Machines_available)) :
        machines.append(Machines_available[i])
    number_of_pairs = len(machines)//2
    alone_machine = len(machines)%2
    while number_of_pairs != 0 :
        winners = []
        for i in range(number_of_pairs) :
            duel = [machines[i],machines[i+1]]
            index = deuxmachines(duel,worker)
            winners.append(duel[index])
            if index == 0 :
                machines.pop(i)
            else :
                machines.pop(i+1)
        winners.append(alone_machine)   
        number_of_pairs = len(machines)//2
        len(machines)%2
    for i in range(len(Machines_available)) : 
        if machines[0] == Machines_available[i] :
            return i
            