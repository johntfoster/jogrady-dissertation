#!/usr/bin/env python

saving = True

import numpy as np
import numpy.ma as ma
import matplotlib

if saving: matplotlib.use('pgf') 

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, MultipleLocator, ScalarFormatter, FuncFormatter

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
plate_length = 2.0
plate_width = 1.0
gamma = -1.0
eps = 1.0e-8


#Load PD plate data
PDfile1name = "plate_reg_50.npz"
PDlabel1 = "101x101 nodes, h10, ext10"
centroids = np.load(PDfile1name)
volumes = centroids['volumes']
nodes = centroids['centroids']
area = (volumes*1000.0)


figureWidth = 5.0
fig=plt.figure(1,figsize=(figureWidth,figureWidth))
ax = fig.add_subplot(111, aspect='equal')
im1 = plt.scatter(nodes[:,0],nodes[:,1],s=area*20000)
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.0])
im1.axes.get_xaxis().set_visible(False)
im1.axes.get_yaxis().set_visible(False)
ax.axis('off')
if saving:
    fig.savefig("../regularMesh50.pgf")

plt.show()

