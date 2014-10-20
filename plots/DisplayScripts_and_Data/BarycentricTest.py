#!/usr/bin/env python

saving = True

import numpy as np
import numpy.ma as ma
import matplotlib
# import numpy.random

if saving: matplotlib.use('pgf') 

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import os
import errno

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if saving:
    font = {'family':'serif',
        'serif':['Times'],
        'size':12}

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

numx = 21
numy = 21
numPts = numx*numy
gridx,gridy = np.meshgrid(np.linspace(-5,5,numx),np.linspace(-5,5,numy))

gridx = gridx.flatten()
gridy = gridy.flatten()
gridz = np.zeros_like(gridx)
grid = np.transpose([gridx,gridy,gridz])

#choose random plane z = c0 + c1*x + c2*y
[c0,c1,c2] = np.random.random_sample([3])
[c0,c1,c2] = [0.1,0.2,0.3]
actualplane = gridx*c1 + gridy*c2 + c0
#choose 3 random points to interpolate from
[A,B,C] = np.hstack((np.random.random([3,2]),[[0.0],[0.0],[0.0]]))
# print "A"
# print A
# print "B"
# print B
# print "C"
# print C
AB = B-A
BA = -AB
AC = C-A
CA = -AC
BC = C-B
CB = -BC

# print "ABxBC",np.cross(AB,BC)

uA = A[0]*c1 + A[1]*c2 + c0
uB = B[0]*c1 + B[1]*c2 + c0
uC = C[0]*c1 + C[1]*c2 + c0

AX = np.asarray(grid - A)
BX = np.asarray(grid - B)
CX = np.asarray(grid - C)
A_cross = np.cross(BC,np.cross(BC,BA))/np.linalg.norm(np.cross(BC,BA))
B_cross = np.cross(CA,np.cross(CA,CB))/np.linalg.norm(np.cross(CA,CB))
C_cross = np.cross(AB,np.cross(AB,AC))/np.linalg.norm(np.cross(AB,AC))
# print "BX",BX
# print "BX shape",np.shape(BX)
# print "A_cross[None,:] shape",np.shape(A_cross[None,:])
Ap = np.inner(BX,A_cross[None,:])
Bp = np.inner(CX,B_cross[None,:])
Cp = np.inner(AX,C_cross[None,:])
totalArea = Ap[0]+Bp[0]+Cp[0]

pointEstimates = (uA*Ap/totalArea + uB*Bp/totalArea +uC*Cp/totalArea ).flatten()
pointErrors = pointEstimates-actualplane.flatten()

# print "Errors"
# print pointErrors
# print "Est Shape"
# print np.shape(pointEstimates)
# print "Err Shape"
# print np.shape(pointErrors)
#exaggerate displacement
scale=1.0
fig=plt.figure()
fig.suptitle('Barycentric Interpolation of Plane',fontsize=16)
ax = fig.add_subplot(211, projection='3d')
ax.plot(gridx,gridy,pointEstimates,ls="None", marker="o",label="Position")
plt.title('Point Estimates')
ax = fig.add_subplot(212, projection='3d')
ax.plot(gridx,gridy,pointErrors,ls="None", marker="o",label="Position")
plt.title('Point Errors')

if saving:
    make_sure_path_exists("./writeup/plots")
    fig.savefig("./writeup/plots/barycentric.pgf")
plt.show()


