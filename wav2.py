#!/usr/bin/python
# -*- coding: utf-8 -*-
import pywt
import scipy.io
import scipy
import matplotlib.pyplot as plt

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


# il faudra avoir 10 images en entrée
mat = scipy.io.loadmat('res.mat')
threeData=mat['threeData']
nbClosedContours=len(threeData[0])

# x, y + angle tangentiel -> 3 colonnes dans chaque
Contour0=threeData[0,0]
Contour1=threeData[0,1]
Contour2=threeData[0,2]

# un signal=Contour0[:,i] pour i de 1 à 3 -> là on fait pour un seul signal
# on calcule le max_level 
nbLevel=pywt.dwt_max_level(len(Contour0), pywt.Wavelet('db3'))-1
coeffs=[[] for i in range(nbLevel+1)] # besoin du niveau au dessus dans les features

#on récupère les abscisses, ordonnées et intégrales des 0 des signaux transformés
points=[[] for i in range(nbLevel+1)] #points[i]=pour un level particulier
for i in range(nbLevel,-1,-1): # besoin de résolution supérieure -> commence par résolution sup
    coeffs[i] = pywt.wavedec(Contour0[:,0], 'db3', level=i+1)
    low=coeffs[i][0]
    high=coeffs[i][1]
    zeroPrec=0
    if(i<nbLevel):
        for j in range(len(high)):
            if(abs(high[j])<0.001):
                a=high[zeroPrec:j]
                zeroPrec=j
                integral=scipy.integrate.simps(a)
                points[i].append([j,integral,coeffs[i+1][0][(j+5)/2]]) # abscisse (1er coeff)  = équivalent dans le premier array ??
#    print points[i]

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


#Determinatin des valeurs optimales -> faut un long set de signatures vraies
# reste a definir dij et Lij
#on fixe Li=4 et on calcule le meilleur Ki
Li=4
minThreshold=1000
Ki=-1
for i in range(1,7): #7?
    Ti=calcThreshold(i,Li)
    if(Ti<minThreshold):
        minThreshold=Ti
        Ki=i

# on prend le Ki déterminé et on calcule le meilleur Li
minThreshold=1000
Li=-1
for i in range(1,nbLevel): # besoin du Level au dessus -> prend un de moins?
    Ti=calcThreshold(Ki,i)
    if(Ti<minThreshold):
        minThreshold=Ti
        Li=i
