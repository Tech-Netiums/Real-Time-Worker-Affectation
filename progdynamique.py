# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:48:04 2020

@author: simon
"""

s = [3,5,8,9]
t = [6,8,7]
m = len(s)
n = len(t) 

pi = [[None for i in range(n+1)] for j in range(m+1)]

former_neighbour = [[None for i in range(n+1)] for j in range(m+1)]

#Modèle sans fatigue
for i in range(m+1) :    
    for j in range(n+1) :
        print(i,j)
        print(pi)
        if (i,j) == (0,0) :
            pi[i][j] = 0
        else :
            
            if i==0 :
                pi[i][j] = pi[i][j-1] + (m+n+1-i-j)*t[j-1]
                former_neighbour[i][j] = (i,j-1)
                
            elif j == 0 :
                pi[i][j] = pi[i-1][j] + (m+n+1-i-j)*s[i-1]
                former_neighbour[i][j] = (i-1,j)
            
            else :
                
                if pi[i][j-1] + (m+n+1-i-j)*t[j-1] < pi[i-1][j] + (m+n+1-i-j)*s[i-1] :
                    pi[i][j] = pi[i][j-1] + (m+n+1-i-j)*t[j-1]
                    former_neighbour[i][j] = (i,j-1)
                    
                else :
                    pi[i][j] = pi[i-1][j] + (m+n+1-i-j)*s[i-1]
                    former_neighbour[i][j] = (i-1,j)

#On reconstruit le chemin                    
path = []
target = former_neighbour[m][n]
path.append(target)
compteur = 0
while target != (0,0) :
    m = target[0]
    n = target[1]
    target = former_neighbour[m][n]
    path.append(target)

path.reverse()
path.append((len(s),len(t)))
