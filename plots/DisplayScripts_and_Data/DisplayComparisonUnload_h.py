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

figureWidth = 6.0

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
gamma = 0.1

analyticalX1 = np.linspace(0.0,1.0,num=1001)
analyticalX2 = np.linspace(0.0,1.0,num=1001)

#Load Abaqus report data
Abaqusfile1name = "./uniformSSunload.rpt"
Abaqusfile1 = open(Abaqusfile1name, "r")
Abaquslines1 = np.loadtxt(Abaqusfile1,skiprows=3)

abaqusX1 = Abaquslines1[:,0]
analyticalX1 = abaqusX1
abaqusY1 = Abaquslines1[:,1]

#Load PD beam data
pdHorizon1 = 0.05
PDfile1name = "./Uniform_L2_EPP18_g2000_h20_n1000_unload_100.npz"
PDlabel1 = "1000 nodes, horizon 0.20"
PDdata1 = np.load(PDfile1name)
ux1 = PDdata1['ux']
uz1 = PDdata1['uz']
health1 = PDdata1['nodeHealth']
pdX1 = ma.masked_outside(ux1,0.0,plate_length)
# analyticalX1 = pdX1
pdZ1 = ma.masked_array(uz1,mask=pdX1.mask)

#Load second PD beam data
pdHorizon2 = 0.05
PDfile2name = "./Uniform_L2_EPP18_g2000_h15_n1000_unload_100.npz"
PDlabel2 = "1000 nodes, horizon 0.15"
PDdata2 = np.load(PDfile2name)
ux2 = PDdata2['ux']
uz2 = PDdata2['uz']
health2 = PDdata2['nodeHealth']
pdX2 = ma.masked_outside(ux2,0.0,plate_length)
analyticalX2 = pdX2
pdZ2 = ma.masked_array(uz2,mask=pdX2.mask)

#Load third PD beam data
pdHorizon3 = 0.05
PDfile3name = "./Uniform_L2_EPP18_g2000_h10_n1000_unload_100.npz"
PDlabel3 = "1000 nodes, horizon 0.10"
PDdata3 = np.load(PDfile3name)
ux3 = PDdata3['ux']
uz3 = PDdata3['uz']
health3 = PDdata3['nodeHealth']
pdX3 = ma.masked_outside(ux3,0.0,plate_length)
analyticalX3 = pdX3
pdZ3 = ma.masked_array(uz3,mask=pdX3.mask)

fig=plt.figure(1,figsize=(figureWidth,figureWidth*3.0/3.0))
plt.hold(True)
ax = fig.add_subplot(111)

ax1=ax.plot(abaqusX1,abaqusY1,label="Abaqus EPP Beam",linestyle="-")
ax2=ax.plot(pdX1,pdZ1,label=PDlabel1,marker="^",markevery=(20,100))
ax3=ax.plot(pdX2,pdZ2,label=PDlabel2,marker=">",markevery=(50,100))
ax4=ax.plot(pdX3,pdZ3,label=PDlabel3,marker="v",markevery=(80,100))

plt.title('Unloaded EPP Beam')
ax.set_xlabel('Distance along Beam')
ax.set_xlim((0.0,2.0))
ax.set_xticks(np.linspace(0.0,2.0,num=5))
ax.set_ylabel('Deflection')
ax.set_ylim(bottom=-1.3e-5,top=0)
ax.set_yticks(1.0e-5*np.linspace(0.0,-1.2,num=5))
ax.grid(True)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.legend(loc=9, borderaxespad=0.)
if saving:
    make_sure_path_exists("../plots")
    fig.savefig("../plots/unloaded2_n1000_g2000_h.pgf")
plt.show()



