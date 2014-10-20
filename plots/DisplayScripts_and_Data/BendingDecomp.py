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
numx = 101
numy = 101
numPts = numx*numy
gridx,gridy = np.meshgrid(np.linspace(-1,1,numx),np.linspace(-1,1,numy))

isobend = gridx**2.0 + gridy**2.0
devbend = gridx**2.0 - gridy**2.0
totbend = isobend+devbend

# gridx = gridx.flatten()
# gridy = gridy.flatten()
# gridz = np.zeros_like(gridx)
# grid = np.transpose([gridx,gridy,gridz])

figureWidth = 10.0
fig=plt.figure(1,figsize=(figureWidth,figureWidth*0.33))
fig.suptitle('Bending Decomposition',fontsize=16)
ax = fig.add_subplot(131, projection='3d')
im = ax.plot_surface(gridx,gridy,totbend,  rstride=5, cstride=5, cmap=plt.cm.rainbow,vmin=-1, vmax=2)
plt.title('Total Bending')
ax = fig.add_subplot(132, projection='3d')
im = ax.plot_surface(gridx,gridy,isobend,  rstride=5, cstride=5, cmap=plt.cm.rainbow,vmin=-1, vmax=2)
plt.title('Isotropic')
ax = fig.add_subplot(133, projection='3d')
im = ax.plot_surface(gridx,gridy,devbend,  rstride=5, cstride=5, cmap=plt.cm.rainbow,vmin=-1, vmax=2)
plt.title('Deviatoric')

plt.show()
if saving:
    make_sure_path_exists("./writeup/plots")
    fig.savefig("./writeup/plots/BendingDecomp.pgf")


