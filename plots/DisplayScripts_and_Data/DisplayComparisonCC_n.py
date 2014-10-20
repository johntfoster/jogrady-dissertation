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

# #Load Abaqus report data
# Abaqusfile1name = "./AbaqusResults/elastic_SSSS_edgeload_10.rpt"
# Abaqusfile1 = open(Abaqusfile1name, "r")
# Abaquslines1 = np.loadtxt(Abaqusfile1,skiprows=19)
# 
# X0a = Abaquslines1[:,1]
# Y0a = Abaquslines1[:,2]
# 
# abaqusZa = Abaquslines1[:,6]
# 
# analyticalXa = X0a
# analyticalYa = Y0a
# analyticalZa = 0.0*X0a
# 
# multiplier = 16.0*(gamma/(plate_length*plate_width))*(yieldstrain/thickness)/(np.pi**6.0)
# for m in range(1,20,2):
#     for n in range(1,20,2):
#         denominator = (m*n*((m/plate_length)**2.0+(n/plate_width)**2.0)**2.0)
#         mnterm =(np.sin(m*np.pi*analyticalXa/plate_length)
#             *np.sin(n*np.pi*analyticalYa/plate_width)
#             /denominator)
#         analyticalZa = analyticalZa+mnterm
# analyticalZa = analyticalZa*multiplier
# 
# difference0 = abaqusZa-analyticalZa

# #Load second Abaqus report data
# Abaqusfile2name = "./AbaqusResults/uniformSSunload.rpt"
# Abaqusfile2 = open(Abaqusfile2name, "r")
# Abaquslines2 = np.loadtxt(Abaqusfile2,skiprows=3)
# 
# abaqusX2 = Abaquslines2[:,0]
# analyticalX2 = abaqusX2
# abaqusY2 = Abaquslines2[:,1]
# abaqusK2 = np.zeros_like(abaqusX2)
# abaqusK2[1:-1]=(abaqusY2[:-2]-2*abaqusY2[1:-1]+abaqusY2[2:])/np.power(abaqusX2[1:-1]-abaqusX2[:-2],2.0)

#Load PD plate data
PDfile1name = "./Clamped_n500_h010_g001_ext04/Clamped_n500_h010_g001_ext04_1_exp_9.npz"
PDlabel1 = "101x101 nodes, h10, ext10"
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


#Load PD plate data
pdHorizon2 = 0.05
PDfile2name = "./Clamped_reweight_n1000_h010_g001_ext02/Clamped_reweight_n1000_h010_g001_ext02_1_exp_16.npz"
PDlabel2 = "101x101 nodes, h05, ext10"
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
analyticalZ2 = analyticalY2 = (gamma*(yieldstrain/thickness)/(24.0*(plate_length**2.0))*(analyticalX2**2.0)*((plate_length-analyticalX2)**2.0))

fig=plt.figure(1,figsize=(figureWidth,figureWidth*3.0/3.0))
plt.hold(True)
ax = fig.add_subplot(111)
ax1=ax.plot(analyticalX2,analyticalZ2,label="Analytical")
ax2=ax.plot(pdX01c,pdZ1c,ls="None", marker="^",markevery=(0,10),label="500 nodes, h=0.01")
ax3=ax.plot(pdX02c,pdZ2c,ls="None", marker="s",markevery=(10,20),label="1000 nodes, h=0.01")
# ax = fig.add_subplot(211, projection='3d')
# ax.plot(analyticalX1,analyticalY1,analyticalZ1,ls="None", marker="o",label="Analytical")
plt.title('Beam Clamped on Each End')

plt.legend(loc=9, borderaxespad=0.)

ax.set_xlabel('Distance Along Plate Centerline')
ax.set_xticks(np.linspace(0.0,1.0,num=5))
ax.set_ylabel('Deflection under Uniform Load')
ax.set_yticks(1.0e-6*np.linspace(0.0,-3,num=6))
ax.grid(True)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

if saving:
    make_sure_path_exists("./writeup/plots")
    fig.savefig("./writeup/plots/clamped_convergence_n.pgf")
plt.show()





