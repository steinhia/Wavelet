#!/usr/bin/python
# -*- coding: utf-8 -*-
import pywt
import scipy.io
import scipy
import matplotlib.pyplot as plt

def di(L,k,s):
    return 1

def d(L,K,S):
    res=0
    for k in range(len(K)):
        for s in range(len(S)):
            res+=di(L,k,s);
    return res

def DissimilarityDegree(I,I1,Threshold):
    dissDegree=d(Li,I,I1)
    return(dissDegree<Threshold)

def calculateNumberClosedContours(Ki):
    NCC=1;
    if(NCC<Ki):
        return [False, NCC]
    else:
        return [True, NCC]

def compareCOntourLength(I,I1):
    ##
    return True

# initialisation des données
# signature à tester
I=[]
# signatures référence
IRef=[]
#nombre optimal Ki
Ki=100
# Threshold optimal
Ti=0.1

# Step 1  Calculate the total number of closed contours in I. If this number is less than K i ( the optimal    larger closed contour number for writer i ), then reject I .
[NCC,Continue]=calculateNumberClosedContours(Ki)


# Step 2  Compare the boundary lengths for each closed contour pair. To speed up the verification process, we use the length of every closed contour as a feature to discard dissimilar reference signatures  before using DTW for verification.
res=False
if(Continue):
    for I1 in IRef:
        if(compareCOntourLength(I,I1)):
# Step 3 Calculate the dissimilarity degree d I between I and all the remaining signatures
# Step 4 Compare d I with a preset dynamic threshold value T i for writer i. If d I v T i , then accept the   signature; otherwise, reject it.
            dd=DissimilarityDegree(I,I1,Ti)
            if(dd):
                res=True   

if(res):
    print "Signature authentique"

else:
    print "Signature falsifiée"
