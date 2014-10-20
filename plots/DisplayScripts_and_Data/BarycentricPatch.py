#!/usr/bin/env python

saving = False

import numpy as np
import numpy.ma as ma
import matplotlib
from matplotlib import collections  as mc
import scipy.sparse
import scipy.spatial
import scipy.optimize
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
numx = 10
numy = 10
numPts = numx*numy
gridx,gridy = np.meshgrid(np.linspace(0,1,numx),np.linspace(0,1,numy))
gridx = gridx.flatten()
# print gridx
gridy = gridy.flatten()
gridz = np.zeros_like(gridx)
grid = np.transpose([gridx,gridy,gridz])
gridnodes = zip(gridx,gridy,gridz)
gridnodesN = np.asarray(gridnodes)
# print "grid"
# print gridnodes
meshnodes = [(0.0,0.0,0.0),(0.0,1.0,0.0),(1.0,1.0,0.0),(1.0,0.0,0.0),(.25,.25,0.0),(.5,.25,0.0),(.6666,.6666,0.0),(.333,.75,0.0)]

# meshnodes = [(0.0,0.0,0.0),(0.0,1.0,0.0),(1.0,1.0,0.0),(1.0,0.0,0.0),(.25,.25,0.0),(.5,.25,0.0),(.6666,.6666,0.0),(.333,.75,0.0),(0.1,0.55,0.0),(0.4,0.5,0.0),(0.6,0.9,0.0),(0.8,0.4,0.0)]
# 
# meshnodes = [(0.0,0.0,0.0),(0.0,1.0,0.0),(1.0,1.0,0.0),(1.0,0.0,0.0),(.25,.25,0.0),(.5,.25,0.0),(.6666,.6666,0.0),(.333,.75,0.0),(0.05,0.55,0.0),(0.1,0.35,0.0),(0.4,0.5,0.0),(0.6,0.9,0.0),(0.85,0.4,0.0),(0.77,0.14,0.0),(0.19,0.84,0.0),(0.9,0.8,0.0)]
# 
# meshnodes = [(0.0,0.0,0.0),(0.0,1.0,0.0),(1.0,1.0,0.0),(1.0,0.0,0.0),
#     (.25,.25,0.0),(.5,.25,0.0),(.6666,.6666,0.0),(.333,.75,0.0),
#     (0.08,0.19,0.0),(0.1,0.55,0.0),(0.19,0.9,0.0),
#     (0.4,0.11,0.0),(0.45,0.5,0.0),(0.55,0.85,0.0),
#     (0.77,0.18,0.0),(0.88,0.43,0.0),(0.91,0.83,0.0)]
#     
# meshnodes = [(0.0,0.0,0.0),(0.0,1.0,0.0),(1.0,1.0,0.0),(1.0,0.0,0.0),
#     (.25,.25,0.0),(.5,.25,0.0),(.6666,.6666,0.0),(.333,.75,0.0),
#     (0.02,0.35,0.0),(0.1,0.55,0.0),
#     (0.4,0.11,0.0),(0.6,0.05,0.0),
#     (0.77,0.18,0.0),(0.88,0.43,0.0),(0.91,0.83,0.0)]
#     

meshnodes = [(0.0,0.0,0.0),(0.0,1.0,0.0),(1.0,1.0,0.0),(1.0,0.0,0.0),
    (.25,.25,0.0),(.5,.25,0.0),(.6666,.6666,0.0),(.333,.75,0.0),
    (0.6,0.05,0.0),(0.4,.95,0.0),(0.05,0.6,0.0),(.95,0.4,0.0)]
    
meshnodesN = np.asarray(meshnodes)
# fig=plt.figure()
# plt.plot(meshnodesN[:,0],meshnodesN[:,1],ls="None", marker="o")
# plt.show()
# xxx
# meshnodesX = meshnodesN[:,0]
# print meshnodesX
# # plotnodes = np.flatten([[0,1],[1,2],[2,3],[3,4],[4,1],[4,5],[3,6],[2,7]])
# plotnodes = [0,1,1,2,2,3,3,4,4,1,4,5,3,6,2,7]
# meshplotX = meshnodesN[plotnodes][:,:2]
# print meshplotX


tree = scipy.spatial.cKDTree(meshnodes)

_, families = tree.query(gridnodes, 
k=3, eps=0.0, p=2)

A = meshnodesN[families[:,0]]
B = meshnodesN[families[:,1]]
C = meshnodesN[families[:,2]]


# fig=plt.figure()
# plt.hold(True)
# plt.plot(meshnodesN[:,0],meshnodesN[:,1],ls="None", marker="o",label="Nodes")
# plt.show()

c0=0.0
c1=1.0
c2=1.0

meshvalues = c0+c1*meshnodesN[:,1]*meshnodesN[:,1]+c2*meshnodesN[:,0]
# print meshvalues
gridvalues = c0+c1*gridnodesN[:,1]*gridnodesN[:,1]+c2*gridnodesN[:,0]

# #choose random plane z = c0 + c1*x + c2*y
# [c0,c1,c2] = np.random.random_sample([3])
# actualplane = gridx*c1 + gridy*c2 + c0
# #choose 3 random points to interpolate from
# [A,B,C] = np.hstack((np.random.random([3,2]),[[0.0],[0.0],[0.0]]))
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

uA = A[:,0]*c1 + A[:,1]*c2 + c0
uB = B[:,0]*c1 + B[:,1]*c2 + c0
uC = C[:,0]*c1 + C[:,1]*c2 + c0
# print "uA"
# print uA
uA = A[:,1]*A[:,1]*c1 + A[:,0]*c2 + c0
uB = B[:,1]*B[:,1]*c1 + B[:,0]*c2 + c0
uC = C[:,1]*C[:,1]*c1 + C[:,0]*c2 + c0
# print "max uA",np.amax(uA)
# print "max uB",np.amax(uB)
# print "max uC",np.amax(uC)

AX = np.asarray(gridnodesN - A)
BX = np.asarray(gridnodesN - B)
CX = np.asarray(gridnodesN - C)

BCBA = np.cross(BC,BA)
CACB = np.cross(CA,CB)
ABAC = np.cross(AB,AC)

A_cross = np.cross(BC,BCBA)/np.sqrt((BCBA*BCBA).sum(axis=-1))[:,None]
B_cross = np.cross(CA,CACB)/np.sqrt((CACB*CACB).sum(axis=-1))[:,None]
C_cross = np.cross(AB,ABAC)/np.sqrt((ABAC*ABAC).sum(axis=-1))[:,None]
# print "shape A_cross",np.shape(A_cross)
# print "BX",BX
# print "BX shape",np.shape(BX)
# print "A_cross[None,:] shape",np.shape(A_cross[None,:])
Ap = (BX*A_cross).sum(axis=-1)
Bp = (CX*B_cross).sum(axis=-1)
Cp = (AX*C_cross).sum(axis=-1)
# print "shape Ap",np.shape(Ap)
totalArea = Ap+Bp+Cp
# print "shape totalArea",np.shape(totalArea)
Ap=Ap/totalArea
Bp=Bp/totalArea
Cp=Cp/totalArea
# print "max Ap",np.amax(Ap)
# print "max Bp",np.amax(Bp)
# print "max Cp",np.amax(Cp)

totalArea = Ap+Bp+Cp

pointEstimates = (uA*Ap + uB*Bp +uC*Cp).flatten()
# print pointEstimates

# actualplane = c0+c1*gridx+c2*gridy
pointErrors = pointEstimates-gridvalues#actualplane.flatten()
maxerror = np.amax(np.absolute(pointErrors))
print "Max error:",maxerror
# print "Errors"
# print pointErrors
# print "Est Shape"
# print np.shape(pointEstimates)
# print "Err Shape"
# print np.shape(pointErrors)
#exaggerate displacement
scale=1.0
fig=plt.figure()
fig.suptitle('Barycentric Interpolation of Quadratic Surface',fontsize=16)
# plt.hold(True)
ax = fig.add_subplot(221, projection='3d')
# ax.scatter(gridx,gridy,c=gridvalues, marker="o",label="Position",vmin=0,vmax=1)
ax.plot(gridx,gridy,gridvalues,ls="None", marker="o",label="Position")
# ax.plot(meshnodesN[:,0],meshnodesN[:,1],ls="None", marker="o",label="Position")
plt.title('Actual Values')

ax = fig.add_subplot(222)
ax.plot(meshnodesN[:,0],meshnodesN[:,1],ls="None", marker="o",label="Position")
plt.title('Real Points')

ax = fig.add_subplot(223, projection='3d')
ax.plot(gridx,gridy,pointEstimates,ls="None", marker="o",label="Position")
# ax.plot(meshnodesN[:,0],meshnodesN[:,1],marker="o")
plt.title('Point Estimates')

ax = fig.add_subplot(224, projection='3d')
# ax.scatter(gridx,gridy,c=np.absolute(pointErrors), marker="o",label="Position",vmin=0,vmax=1)
ax.plot(gridx,gridy,pointErrors,ls="None", marker="o",label="Position")
# ax.plot(gridx,gridy,pointErrors,c=np.absolute(pointErrors/maxerror),ls="None", marker="o",label="Position")
# im2 = ax.plot_surface(gridx,gridy,pointErrors,  rstride=1, cstride=1, cmap=plt.cm.rainbow)
plt.title('Error')


if saving:
    make_sure_path_exists("./writeup/plots")
    fig.savefig("./writeup/plots/baryPatch2.pgf")
plt.show()
