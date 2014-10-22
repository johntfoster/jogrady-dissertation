#!/usr/bin/env python

saving = True

import numpy as np
import numpy.ma as ma
import matplotlib

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

    #Problem parameters
yieldstrain = 1.0e-6
thickness = 0.01
plate_length = 1.0
plate_width = 1.0
gamma = -1.0
eps = 1.0e-8

viewElev = 20.0
viewAzim = -45.0

viewPt = [np.sin(viewAzim*np.pi/180.0)*np.cos(viewElev*np.pi/180.0),
    np.cos(viewAzim*np.pi/180.0)*np.cos(viewElev*np.pi/180.0),
    np.sin(viewElev*np.pi/180.0)]


#Load PD plate data
PDfile1name = "Ring_t001_n20.npz"
PDlabel1 = "101x101 nodes, h10, ext10"
centroids = np.load(PDfile1name)
volumes = centroids['volumes']
nodes = centroids['centroids']
area = (volumes*1000.0)

viewsort = (viewPt*nodes).sum(axis=1).argsort()
nodes = nodes[viewsort]
heights = nodes[:,2]+0.5
# print "heights shape",np.shape(heights)
# print heights

figureWidth = 10.0
fig=plt.figure(1,figsize=(figureWidth,figureWidth))
ax = fig.add_subplot(111, projection='3d', aspect='equal')
ax.plot([0.0],[0.5],[0.0],'w')
ax.plot([0.0],[-0.5],[0.0],'w')
# ax.plot(nodes[:,0],nodes[:,1],nodes[:,2],ls="None", marker="o",color=heights)
# plt.gray()
# ax.scatter(nodes[:,0],nodes[:,1],nodes[:,2], marker="o",depthshade=False)#,color=heights)
ax.scatter(nodes[:,0],nodes[:,1],nodes[:,2], marker="o",color=heights)
ax.view_init(elev=viewElev, azim=viewAzim)
# plt.gray()


ax.axis('off')
plt.tight_layout()
if saving:
    fig.savefig("../RingMesh20.pgf",bbox_inches='tight')

plt.show()


