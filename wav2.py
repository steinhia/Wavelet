#!/usr/bin/python
# -*- coding: utf-8 -*-
import pydtw
import pywt
import scipy.io
import scipy
import matplotlib.pyplot as plt
from verification import di,DissimilarityDegree,calculateNumberClosedContours,compareContourLength,calcThreshold,CalcLi,CalcKi,CalcD,CalcL,DTWDistance
import numpy as np

# structure : 9 images -> K closedContours -> 3 signaux
# pour chaque signal : L levels ->  m tableaux de coeffs par level -> n zero de la transformée -> stocke 3 infos
# donc besoin d'un tableau [i,k,j,l,n,t]
# i le numero de l'image
# k le nombre de closed contours
# j le numéro du signal (x,y,tangential angle)
# l le level
# n zeros de la transformée
# pour chaque t indice parmi les 3 infos
# a chaque fois Features[i,k,j,l].append([.,.,.])
# Features est de taille 9 * nbClosedContours * 3 * LevelMax * un certain nombre (les zeros) *3

def verification(Features,Ki,Li,Ti,numSign,nbImg): #TODO : verifier que c'est correct

    # Step 1  Calculate the total number of closed contours in I. If this number is less than K i ( the optimal larger closed contour number for writer i ), then reject I .
    [NCC,Continue]=calculateNumberClosedContours(Features,numSign,Ki) #OK

    # Step 2  Compare the boundary lengths for each closed contour pair. To speed up the verification process, we use the length of every closed contour as a feature to discard dissimilar reference signatures  before using DTW for verification.
    if(Continue):
        for i in range(nbImg):
            if(i!=numSign and compareContourLength(i,numSign,Features)):
# Step 3 Calculate the dissimilarity degree d I between I and all the remaining signatures
# Step 4 Compare d I with a preset dynamic threshold value T i for writer i. If d I v T i , then accept the   signature; otherwise, reject it.
                dd=DissimilarityDegree(i,numSign,Features,Ki,Li)
                if(dd<Ti):
                    return True
    return False


def CalcFeatures(threeData10): #TODO : verifier que c'est correct :/
    nbImg=len(threeData10)
    numImage=0
    threeData=threeData10[0] # première image
    nCC=[-1] * nbImg #nb Closed Contours
    for i in range(nbImg):
        nCC[i]=len(threeData10[i][0][0]) # nb de closed Contours par image, 0 à cause de matlab
        # tableau contenant toutes les features
        Features=[[[[[] for l in range(pywt.dwt_max_level(len(threeData10[i][0][0][k][:,j]), pywt.Wavelet('db3'))-1)] for j in range(3) ] for k in range(nCC[i])] for i in range(nbImg)] 
        for i in range(nbImg):
            for k in range(nCC[i]):
                # x,y et tangential angle
                d=threeData10[i][0][0][k]
                Signal=[d[:,0],d[:,1],d[:,2]] # pour ce contour, x y et tanAngle

                # on calcule le max_level 
                sizeLevel=len(d[:,0])
                nbLevel=pywt.dwt_max_level((sizeLevel), pywt.Wavelet('db3'))-1
                coeffs=[[] for s in range(nbLevel+1)] # faut pouvoir prendre celui du dessus
                for j in range(3): # pour chacun de ces 3 x y et tanAngle
                    for l in range(nbLevel,-1,-1): # besoin de res sup -> commence par résolution max
                        #on récupère les abscisses, ordonnées et intégrales des 0 des signaux transformés
                        wavedec=pywt.wavedec(Signal[j], 'db3', level=l+1)
                        low=wavedec[0]
                        high=wavedec[1]
                        coeffs[l]=wavedec
                        zeroPrec=0
                        if(l<nbLevel):
                            for m in range(len(high)):
                                if(abs(high[m])<0.001): # verifier ici
                                    a=high[zeroPrec:m]
                                    zeroPrec=m
                                    if(len(a)>0):
                                        integral=scipy.integrate.simps(a)
                                    else:
                                        integral=0
                                    absCorr=(m+5)/2
                                    if(absCorr>=len(coeffs[l+1][0])):
                                        absCorr=len(coeffs[l+1][0])-1
                                    if(absCorr<0):
                                        abscCorr=0
                                    Features[i][k][j][l].append([j,integral,absCorr]) # abscisse (1er coeff)  = équivalent dans le premier array ?? #TODO bonnes abscisses
    return Features


# Calcul des features sur les env10 images de la base, dont celle qu'on veut vérifier
# (l'avant dernière pour 'instant pour simplifier)
mat = scipy.io.loadmat('res.mat')
threeData10=mat['threeData10']
nbImg=len(threeData10)
Features=CalcFeatures(threeData10)

#Determinatin des valeurs optimales
numSign=nbImg-1 
Ki=CalcKi(nbImg,numSign,Features)
[Li,Ti]=CalcLi(4,nbImg,numSign,Ki,Features) #TODO : 4 pour nbLevel?

# verification de la dernière signature
#for numSign in range(nbImg-1): #TODO : enlever la signature test des calc valeurs opti
# verification d'une certaine signature
verif=verification(Features,Ki,Li,Ti,numSign,nbImg)#nbImg-1 = numTest
if(verif):
    print "Signature authentique"

else:
    print "Signature falsifiée"












# pour se rendre compte des coefficients et les longuers des arrays
# print "\n"   longueur = (niveauSup+5)/2 pour db3 -> int(w.dec_len)

# print "level =5"
# print len(coeffs[4][0]) #15
# print len(coeffs[4][1]) #15
# print len(coeffs[4][2]) #25
# print len(coeffs[4][3]) #45
# print len(coeffs[4][4]) #86
# print len(coeffs[4][5]) #167



# print "level =4"
# print len(coeffs[3][0]) #25
# print len(coeffs[3][1]) #25
# print len(coeffs[3][2]) #45
# print len(coeffs[3][3]) #86
# print len(coeffs[3][4]) #167

# print "level =3"
# print len(coeffs[2][0]) 45
# print len(coeffs[2][1]) 45
# print len(coeffs[2][2]) 86
# print len(coeffs[2][3]) 167

# print "level =2"
# print len(coeffs[1][0])
# print len(coeffs[1][1])
# print len(coeffs[1][2])

# print "level =1"
# print len(coeffs[1][0])
# print len(coeffs[1][1])
# print len(coeffs[1][2])

# plt.plot(coeffs[4][0]) # lowpass 2* + court
# plt.show()
# plt.plot(coeffs[4][1]) # lowpass 2* + court
# plt.show()




