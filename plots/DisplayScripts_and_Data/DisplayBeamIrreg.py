#!/usr/bin/env python

saving = False

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

figureWidth = 6.0

    #Problem parameters
yieldstrain = 1.0e-3
thickness = 0.001
plate_length = 1.0
plate_width = 1.0
gamma = -0.001
eps = 1.0e-6

analyticalX1 = np.linspace(0.0,1.0,num=1001)
analyticalX2 = np.linspace(0.0,1.0,num=1001)

#Load PD plate data
PDfile1name = "./SSbeam_U_regular_200_1_exp_14.npz"
PDlabel1 = "regular 100 nodes, horizon 0.05"
PDdata1 = np.load(PDfile1name)
ux1 = PDdata1['ux']
uy1 = PDdata1['uy']
uz1 = PDdata1['uz']
x01 = PDdata1['x0']
y01 = PDdata1['y0']

data1mask = np.logical_or(0.0-eps>x01,plate_length+eps<x01)

pdX1 = ma.array(ux1,mask=data1mask)
pdY1 = ma.array(uy1,mask=data1mask)
pdZ1 = ma.array(uz1,mask=data1mask)

pdX1c=pdX1.compressed()
pdY1c=pdY1.compressed()
pdZ1c=pdZ1.compressed()

pdX01 = ma.array(x01,mask=data1mask)
pdY01 = ma.array(y01,mask=data1mask)
pdX01c=pdX01.compressed()
pdY01c=pdY01.compressed()

#Elastic Displacement for uniform load of gamma
analyticalX1 = pdX01c
analyticalY1 = pdY01c
# analyticalZ1 = [((gamma*yieldstrain/(24.0*thickness*plate_length**2))*
#     (x**2.0-4.0*x*plate_length+6.0*plate_length**2)*x**2.0) for x in analyticalX1]

multiplier = gamma*(yieldstrain/thickness)/(24.0*(plate_length**2.0))
center = analyticalX1*(plate_length**3.0-2*(analyticalX1**2.0)*plate_length+analyticalX1**3.0)
analyticalZ1 = center*multiplier    

difference1 = pdZ1c-analyticalZ1


#Load PD plate data
pdHorizon2 = 0.05
PDfile2name = "./SSbeam_U_irregular_200_1_exp_9.npz"
PDlabel2 = "irregular 100 nodes, horizon 0.05"
PDdata2 = np.load(PDfile2name)
ux2 = PDdata2['ux']
uy2 = PDdata2['uy']
uz2 = PDdata2['uz']
x02 = PDdata2['x0']
y02 = PDdata2['y0']

data2mask = np.logical_or(0.0-eps>x02,plate_length+eps<x02)

pdX2 = ma.array(ux2,mask=data2mask)
pdY2 = ma.array(uy2,mask=data2mask)
pdZ2 = ma.array(uz2,mask=data2mask)

pdX2c=pdX2.compressed()
pdY2c=pdY2.compressed()
pdZ2c=pdZ2.compressed()

pdX02 = ma.array(x02,mask=data2mask)
pdY02 = ma.array(y02,mask=data2mask)
pdX02c=pdX02.compressed()
pdY02c=pdY02.compressed()

#Elastic Displacement for uniform load of gamma
analyticalX2 = pdX02c
analyticalY2 = pdY02c
# analyticalZ2 = [((gamma*yieldstrain/(24.0*thickness*plate_length**2))*
#     (x**2.0-4.0*x*plate_length+6.0*plate_length**2)*x**2.0) for x in analyticalX2]
    
multiplier = gamma*(yieldstrain/thickness)/(24.0*(plate_length**2.0))
center = analyticalX2*(plate_length**3.0-2*(analyticalX2**2.0)*plate_length+analyticalX2**3.0)
analyticalZ2 = center*multiplier
    
difference2 = pdZ2c-analyticalZ2

fig=plt.figure(1,figsize=(figureWidth,figureWidth*3.0/3.0))
plt.hold(True)
ax = fig.add_subplot(111)
ax.plot(analyticalX1,analyticalZ1,ls="-",label="Analytical")
ax1=ax.plot(pdX01c,pdZ1c,ls="None", marker="^",markevery=(0,6),label="regular discretization")
ax1=ax.plot(pdX02c,pdZ2c,ls="None", marker="s",markevery=(3,6),label="irregular discretization")
# ax1=ax.plot(pdX02c,analyticalZ2,ls="None", marker="s",markevery=(2,4),label="irregular error")
# ax = fig.add_subplot(211, projection='3d')
# ax.plot(analyticalX1,analyticalY1,analyticalZ1,ls="None", marker="o",label="Analytical")
# plt.title('Uniformly Loaded Beam')

plt.legend(loc=9, borderaxespad=0.)

ax.set_xlabel('Distance Along Beam')
ax.set_xticks(np.linspace(0.0,1.0,num=5))
ax.set_ylabel('Deflection Under Uniform Load')
# ax.set_yticks(1.0e-4*np.linspace(0.0,-1.4,num=5))
# ax.set_ylim([-0.00014,0.0])
ax.grid(True)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

if saving:
#     make_sure_path_exists("./writeup/plots")
    fig.savefig("../IrregularBeam.pgf")
plt.show()








