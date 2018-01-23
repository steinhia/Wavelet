#!/usr/bin/python
# -*- coding: utf-8 -*-
import pywt
import scipy.io
import scipy
import matplotlib.pyplot as plt


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

#calcul de Ti en fonction de Li et Ki, pour writer i
def calcThreshold(Ki,Li):
    # TODO trouver Lij et dij
    # dij distance avec le voisin le plus proche parmi n-1 autres, writer i, signature j
    # Lij : total length (in pixels) of the 1st Ki longest closed contours in the ref signature j
    dij=0.5
    Lij=2
    nWriters=10
    delta=2
    Mu=0
    Sigma=0
    for i in range(nWriters):
        Mu+=dij/Lij
    Mu/=nWriters
    for i in range(nWriters):
        Sigma+=((dij-Mu)/Lij)**2
    Sigma/=(nWriters-1)
    return Mu+2*Sigma

def CalcLi(nbLevel):
    # on prend le Ki déterminé et on calcule le meilleur Li
    minThreshold=1000
    Li=-1
    for i in range(1,nbLevel): # besoin du Level au dessus -> prend un de moins?
        Ti=calcThreshold(Ki,i)
        if(Ti<minThreshold):
            minThreshold=Ti
            Li=i


def CalcKi():
   # reste a definir dij et Lij
   # on fixe Li=4 et on calcule le meilleur Ki
    Li=4
    minThreshold=1000
    Ki=-1
    for i in range(1,7): #7?
        Ti=calcThreshold(i,Li)
        if(Ti<minThreshold):
            minThreshold=Ti
            Ki=i


def CalcFeatures(threeData10):
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
                                if(abs(high[m])<0.001): # verifier ici, et comment avoir res >
                                    a=high[zeroPrec:m]
                                    zeroPrec=m
                                    if(len(a)>0):
                                        integral=scipy.integrate.simps(a)
                                    else:
                                        integral=0
                                        abscCorr=(m+5)/2
                                        if(abscCorr>=len(coeffs[l+1][0])):
                                            abscCorr=len(coeffs[l+1][0])-1
                                            if(abscCorr<0):
                                                abscCorr=0
                                                Features[i][k][j][l].append([j,integral,abscCorr]) # abscisse (1er coeff)  = équivalent dans le premier array ??
    return Features



# il faudra passer les 10 images en entrée, on commence avec la première image
mat = scipy.io.loadmat('res.mat')
threeData10=mat['threeData10']
Features=CalcFeatures(threeData10)

#Determinatin des valeurs optimales -> faut un long set de signatures vraies
Ki=CalcKi()
Li=CalcLi(4)








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



