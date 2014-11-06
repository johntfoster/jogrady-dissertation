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
gamma = 20.0

analyticalX1 = np.linspace(0.0,1.0,num=1001)
analyticalX2 = np.linspace(0.0,1.0,num=1001)

#Load Abaqus report data
Abaqusfile1name = "./uniformElasticSS20.rpt"
Abaquslabel1 = "Abaqus Elastic Beam"
Abaqusfile1 = open(Abaqusfile1name, "r")
Abaquslines1 = np.loadtxt(Abaqusfile1,skiprows=3)

abaqusX1 = Abaquslines1[:,0]
analyticalX1 = abaqusX1
abaqusY1 = Abaquslines1[:,1]

#Load PD beam data
pdHorizon1 = 0.05
PDfile1name = "./Uniform_Elastic_g2000_h20_n50_25.npz"
PDlabel1 = "50 nodes, horizon 0.20"
PDdata1 = np.load(PDfile1name)
ux1 = PDdata1['ux']
uz1 = PDdata1['uz']
health1 = PDdata1['nodeHealth']
pdX1 = ma.masked_outside(ux1,0.0,plate_length)
# analyticalX1 = pdX1
pdZ1 = ma.masked_array(uz1,mask=pdX1.mask)
pdHealth1 = ma.masked_array(health1,mask=pdX1.mask)

#Load second PD beam data
pdHorizon2 = 0.05
PDfile2name = "./Uniform_Elastic_g2000_h20_n100_25.npz"
PDlabel2 = "100 nodes, horizon 0.20"
PDdata2 = np.load(PDfile2name)
ux2 = PDdata2['ux']
uz2 = PDdata2['uz']
health2 = PDdata2['nodeHealth']
pdX2 = ma.masked_outside(ux2,0.0,plate_length)
analyticalX2 = pdX2
pdZ2 = ma.masked_array(uz2,mask=pdX2.mask)
pdHealth2 = ma.masked_array(health2,mask=pdX2.mask)


#Elastic Displacement for uniform load of gamma
analyticalY2 = [((-gamma*yieldstrain/(24.0*thickness*plate_length**2))*
    (x**4.0-2.0*(x**3)*plate_length+x*plate_length**3)) for x in analyticalX2]
    
#     ((-gamma*yieldstrain/(24.0*thickness*plate_length**2))*
#      (xvector**2.0-4.0*xvector*plate_length+6.0*plate_length**2)*xvector**2.0)

# Compare on one plot 

fig=plt.figure(1,figsize=(figureWidth,figureWidth*3.0/3.0))
plt.hold(True)
ax = fig.add_subplot(111)
ax1=ax.plot(analyticalX2,analyticalY2,label=r"Analytical",linestyle="-",marker="o",markevery=(0,10))
ax2=ax.plot(pdX1,pdZ1,label=r"50 nodes, $\delta = 0.20$",marker="^",markevery=(2,5))
ax3=ax.plot(pdX2,pdZ2,label=r"100 nodes, $\delta = 0.20$",marker=">",markevery=(7,10))

# plt.title('Uniformly Loaded Elastic Beam')
ax.set_xlabel('Distance along Beam')
ax.set_xlim((0.0,2.0))
ax.set_xticks(np.linspace(0.0,2.0,num=5))
ax.set_ylabel('Deflection')
ax.set_ylim(top=0)
ax.set_yticks(1.0e-4*np.linspace(0.0,-1.2,num=5))
ax.grid(True)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# plt.ylim((-.0000001,0.0))
# plt.legend(loc=3, borderaxespad=0.)
plt.legend(loc=9, borderaxespad=0.)
if saving:
    make_sure_path_exists("../plots")
    fig.savefig("../elastic_h20_g2000.pgf")
plt.show()



