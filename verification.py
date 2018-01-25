#!/usr/bin/python
# -*- coding: utf-8 -*-
import pydtw
import scipy.io
import scipy
import matplotlib.pyplot as plt

# dynamic time warping entre i et j pour comparer 2 closed contours de longueur diff
def di(L,k,s,i,j): #TODO
    return 1

# diss degree entre 2 signatures, utilisé pour le train et test
def DissimilarityDegree(i,j,Features,Ki,Li): #TODO
    S=[]
    res=0
    for k in range(Ki): # compare 2 closed contours, de nuéro k
        for s in range(len(S)): # x, y et angle tangentiel, ou données wavelet?
            res+=di(Li,k,s,i,j);
    return res

def calculateNumberClosedContours(Features,numSign,Ki): #DONE
    NCC=len(Features[numSign]);
    if(NCC<Ki):
        return [False, NCC]
    else:
        return [True, NCC]

def compareContourLength(i,numSign,Features): #TODO
    Contouri=len(Features[i]) #nb de ClosedContour
    ContourNumSign=len(Features[numSign])
    #faut comparer les ClosedContours par paires
    # avec ma base nombre trop différent (14 closedContours?),faut prendre une autre base
    # mais regarder comment faire avec un nombre différent de contours
    return True

#calcul de Ti en fonction de Li et Ki, pour writer i
def calcThreshold(Ki,Li,nbImg,numSign,d,L): #TODO verifier que c'est correct
    # dij distance avec le voisin le plus proche parmi n-1 autres, writer i, signature j
    # Lij : total length (in pixels) of the 1st Ki longest closed contours in the ref signature j
    delta=2 # l'article le fixe a deux
    Mu=0
    Sigma=0
    for i in range(nbImg): #on teste sur la dernière, donc ici pas prise en cpte(train)
        if(i!=numSign):
            Mu+=d[i]/L[i]
    Mu/=nbImg
    for i in range(nbImg):
        if(i!=numSign):
            Sigma+=((d[i]-Mu)/L[i])**2
    Sigma/=(nbImg-2)# enlève image de test et -1 dans la formule
    return Mu+2*Sigma

def CalcLi(nbLevel,nbImg,numSign,Ki,Features):
    # on prend le Ki déterminé et on calcule le meilleur Li
    minThreshold=1000
    Li=-1
    for i in range(1,nbLevel): # quel level? le min des maxLevel utilisés?  TODO
        d=CalcD(Features,nbImg,Ki,i)
        L=CalcL(Features,nbImg,Ki,i)
        Ti=calcThreshold(Ki,i,nbImg,nbImg-1,d,L)
        if(Ti<minThreshold):
            minThreshold=Ti
            Li=i
    return [Li,minThreshold]


def CalcKi(nbImg,numSign,Features):
   # reste a definir Lij
   # on fixe Li=4 et on calcule le meilleur Ki
    Li=4
    minThreshold=1000
    Ki=-1
    for i in range(1,7): # TODO quel range? Ki=i
        #détermination des dj et Lj à partir des features
        d=CalcD(Features,nbImg,i,Li)
        L=CalcL(Features,nbImg,i,Li)
        Ti=calcThreshold(i,Li,nbImg,numSign,d,L) # on teste l'image numSign
        if(Ti<minThreshold):
            minThreshold=Ti
            Ki=i
    return Ki

    #calcule toutes les distances aux autres, y compris image test aux autres
def CalcD(Features,nbImg,Ki,Li): 
    # dij dist ac le voisin le + proche parmi n-1 autres, writer i (nous0), signature j
    d=[1000]*nbImg
    for j in range(nbImg): #on cherche dj
        for k in range(nbImg): # on compare j avec tous les voisins
            if(k!=j): 
                dd=DissimilarityDegree(j,k,Features,Ki,Li)
                if(dd<d[j]):
                    d[j]=dd
    return d

def CalcL(Features,nbImg,Ki,Li): #TODO
    L=[1]*nbImg
    return L




def DTWDistance(s, t) :
    n=len(s)
    m=len(t)
    DTW=[[[]for j in range(m+1)]for i in range(n+1)]

    for i in range(1,n+1):
        DTW[i][0] = 100000
    for i in range(1,m+1):
        DTW[0][i] = 100000
    DTW[0][0]= 0

    for i in range(1,n+1):
        for j in range(1,m+1):
            cost = abs(s[i-1]-t[j-1])
            DTW[i][j]=cost + min(DTW[i-1][j],    # insertion
                                       DTW[i][j-1],    #deletion
                                       DTW[i-1][j-1])    #match
    return DTW[n][m]






