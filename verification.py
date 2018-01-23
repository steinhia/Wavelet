#!/usr/bin/python
# -*- coding: utf-8 -*-
import pywt
import scipy.io
import scipy
import matplotlib.pyplot as plt

def di(L,k,s): #TODO
    return 1

def d(L,K,S): #TODO
    res=0
    for k in range(len(K)):
        for s in range(len(S)):
            res+=di(L,k,s);
    return res

def DissimilarityDegree(i,numSign,Features,Ti,Li): #TODO : calcul des dij? (nous on a un seul i)
    I=[]
    I1=[]
    dissDegree=d(Li,I,I1)
    return(dissDegree<Ti)

def calculateNumberClosedContours(Features,numSign,Ki): #DONE
    NCC=len(Features[numSign]);
    print NCC
    if(NCC<Ki):
        return [False, NCC]
    else:
        return [True, NCC]

def compareContourLength(i,numSign,Features): #TODO
    Contouri=len(Features[i]) #nb de ClosedContour
    ContourNumSign=len(Features[numSign])
    #faut comparer les ClosedContours par paires
    # avec ma base nombre trop différent, faut prendre une autre base
    # mais regarder comment faire avec un nombre différent de contours
    return True

#calcul de Ti en fonction de Li et Ki, pour writer i
def calcThreshold(Ki,Li,nbImg,d,L): #TODO verifier que c'est correct
    # dij distance avec le voisin le plus proche parmi n-1 autres, writer i, signature j
    # Lij : total length (in pixels) of the 1st Ki longest closed contours in the ref signature j
    delta=2 # l'article le fixe a deux
    Mu=0
    Sigma=0
    for i in range(nbImg-1): # on teste sur la derniere
        Mu+=d[i]/L[i]
    Mu/=nbImg
    for i in range(nbImg-1):
        Sigma+=((d[i]-Mu)/L[i])**2
    Sigma/=(nbImg-2)
    return Mu+2*Sigma

def CalcLi(nbLevel,nbImg,d,L,Ki):
    # on prend le Ki déterminé et on calcule le meilleur Li
    minThreshold=1000
    Li=-1
    for i in range(1,nbLevel): # quel level? le min des maxLevel utilisés?  TODO
        Ti=calcThreshold(Ki,i,nbImg-1,d,L)
        if(Ti<minThreshold):
            minThreshold=Ti
            Li=i
    return [Li,minThreshold]


def CalcKi(nbImg,d,L):
   # reste a definir dij et Lij
   # on fixe Li=4 et on calcule le meilleur Ki
    Li=4
    minThreshold=1000
    Ki=-1
    for i in range(1,7): # TODO quel range?
        Ti=calcThreshold(i,Li,nbImg-1,d,L)
        if(Ti<minThreshold):
            minThreshold=Ti
            Ki=i
    return Ki

    # TODO trouver Lij et dij -> dans Features -> quelle distance?
def CalcD(Features,nbImg): #TODO
    d=[1]*nbImg
    return d


def CalcL(Features,nbImg): #TODO
    L=[1]*nbImg
    return L








