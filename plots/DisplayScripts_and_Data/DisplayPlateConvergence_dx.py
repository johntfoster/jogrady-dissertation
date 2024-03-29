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
thickness = 0.01
plate_length = 1.0
plate_width = 1.0
gamma = -0.1
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
PDfile1name = "./Nu33_n41_h05_g0pt1_1_exp_8.npz"
PDlabel1 = "101x101 nodes, h10, ext10"
PDdata1 = np.load(PDfile1name)
ux1 = PDdata1['ux']
uy1 = PDdata1['uy']
uz1 = PDdata1['uz']
x01 = PDdata1['x0']
y01 = PDdata1['y0']

data1mask = np.logical_or(
    np.logical_or(0.0-eps>x01,plate_length+eps<x01),
    np.logical_or((plate_width/2.0)-eps>y01,(plate_width/2.0)+eps<y01))

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
analyticalZ1 = 0.0*pdZ1c
multiplier = 16.0*(gamma/(plate_length*plate_width))*(yieldstrain/thickness)/(np.pi**6.0)
for m in range(1,20,2):
    for n in range(1,20,2):
        denominator = (m*n*((m/plate_length)**2.0+(n/plate_width)**2.0)**2.0)
        mnterm =(np.sin(m*np.pi*analyticalX1/plate_length)
            *np.sin(n*np.pi*analyticalY1/plate_width)
            /denominator)
        analyticalZ1 = analyticalZ1+mnterm
analyticalZ1 = analyticalZ1*multiplier

difference1 = pdZ1c-analyticalZ1

#Load PD plate data
pdHorizon2 = 0.05
PDfile2name = "./Nu33_n51_h05_g0pt1_1_exp_8.npz"
PDlabel2 = "101x101 nodes, h05, ext10"
PDdata2 = np.load(PDfile2name)
ux2 = PDdata2['ux']
uy2 = PDdata2['uy']
uz2 = PDdata2['uz']
x02 = PDdata2['x0']
y02 = PDdata2['y0']

data2mask = np.logical_or(
    np.logical_or(0.0-eps>x02,plate_length+eps<x02),
    np.logical_or((plate_width/2.0)-eps>y02,(plate_width/2.0)+eps<y02))

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
analyticalZ2 = 0.0*pdZ2c
multiplier = 16.0*(gamma/(plate_length*plate_width))*(yieldstrain/thickness)/(np.pi**6.0)
for m in range(1,10,2):
    for n in range(1,10,2):
        denominator = (m*n*((m/plate_length)**2.0+(n/plate_width)**2.0)**2.0)
        mnterm =(np.sin(m*np.pi*analyticalX2/plate_length)
            *np.sin(n*np.pi*analyticalY2/plate_width)
            /denominator)
        analyticalZ2 = analyticalZ2+mnterm
analyticalZ2 = analyticalZ2*multiplier

difference2 = pdZ2c-analyticalZ2

#Load PD plate data
pdHorizon3 = 0.05
PDfile3name = "./Nu33_n61_h05_g0pt1_1_exp_7.npz"
PDlabel3 = "101x101 nodes, h05, ext10"
PDdata3 = np.load(PDfile3name)
ux3 = PDdata3['ux']
uy3 = PDdata3['uy']
uz3 = PDdata3['uz']
x03 = PDdata3['x0']
y03 = PDdata3['y0']

data3mask = np.logical_or(
    np.logical_or(0.0-eps>x03,plate_length+eps<x03),
    np.logical_or((plate_width/2.0)-eps>y03,(plate_width/2.0)+eps<y03))

pdX3 = ma.array(ux3,mask=data3mask)
pdY3 = ma.array(uy3,mask=data3mask)
pdZ3 = ma.array(uz3,mask=data3mask)

pdX3c=pdX3.compressed()
pdY3c=pdY3.compressed()
pdZ3c=pdZ3.compressed()

pdX03 = ma.array(x03,mask=data3mask)
pdY03 = ma.array(y03,mask=data3mask)
pdX03c=pdX03.compressed()
pdY03c=pdY03.compressed()

#Elastic Displacement for uniform load of gamma
analyticalX3 = pdX03c
analyticalY3 = pdY03c
analyticalZ3 = 0.0*pdZ3c
multiplier = 16.0*(gamma/(plate_length*plate_width))*(yieldstrain/thickness)/(np.pi**6.0)
for m in range(1,10,2):
    for n in range(1,10,2):
        denominator = (m*n*((m/plate_length)**2.0+(n/plate_width)**2.0)**2.0)
        mnterm =(np.sin(m*np.pi*analyticalX3/plate_length)
            *np.sin(n*np.pi*analyticalY3/plate_width)
            /denominator)
        analyticalZ3 = analyticalZ3+mnterm
analyticalZ3 = analyticalZ3*multiplier

difference3 = pdZ3c-analyticalZ3


#Load PD plate data
pdHorizon4 = 0.05
PDfile4name = "./Nu33_n81_h05_g0pt1_1_exp_7.npz"
PDlabel4 = "101x101 nodes, h05, ext10"
PDdata4 = np.load(PDfile4name)
ux4 = PDdata4['ux']
uy4 = PDdata4['uy']
uz4 = PDdata4['uz']
x04 = PDdata4['x0']
y04 = PDdata4['y0']

data4mask = np.logical_or(
    np.logical_or(0.0-eps>x04,plate_length+eps<x04),
    np.logical_or((plate_width/2.0)-eps>y04,(plate_width/2.0)+eps<y04))

pdX4 = ma.array(ux4,mask=data4mask)
pdY4 = ma.array(uy4,mask=data4mask)
pdZ4 = ma.array(uz4,mask=data4mask)

pdX4c=pdX4.compressed()
pdY4c=pdY4.compressed()
pdZ4c=pdZ4.compressed()

pdX04 = ma.array(x04,mask=data4mask)
pdY04 = ma.array(y04,mask=data4mask)
pdX04c=pdX04.compressed()
pdY04c=pdY04.compressed()

#Elastic Displacement for uniform load of gamma
analyticalX4 = pdX04c
analyticalY4 = pdY04c
analyticalZ4 = 0.0*pdZ4c
multiplier = 16.0*(gamma/(plate_length*plate_width))*(yieldstrain/thickness)/(np.pi**6.0)
for m in range(1,10,2):
    for n in range(1,10,2):
        denominator = (m*n*((m/plate_length)**2.0+(n/plate_width)**2.0)**2.0)
        mnterm =(np.sin(m*np.pi*analyticalX4/plate_length)
            *np.sin(n*np.pi*analyticalY4/plate_width)
            /denominator)
        analyticalZ4 = analyticalZ4+mnterm
analyticalZ4 = analyticalZ4*multiplier


fig=plt.figure(1,figsize=(figureWidth,figureWidth*3.0/3.0))
plt.hold(True)
ax = fig.add_subplot(111)
# ax1=ax.plot(analyticalX1,analyticalZ1,label="Analytical")
# ax1=ax.plot(pdX1c,pdZ1c,ls="None", marker="^",markevery=(0,2),label=r"$\Delta x$=0.025, h=0.05")
ax1=ax.plot(pdX1c,pdZ1c,ls="None", marker="^",markevery=(0,4),label=r"40 nodes/side, $\delta=0.05$")
ax2=ax.plot(pdX2c,pdZ2c,ls="None", marker="o",markevery=(1,5),label=r"50 nodes/side, $\delta=0.05$")
ax3=ax.plot(pdX3c,pdZ3c,ls="None", marker="v",markevery=(3,6),label=r"60 nodes/side, $\delta=0.05$")
ax4=ax.plot(pdX4c,pdZ4c,ls="None", marker="s",markevery=(6,8),label=r"80 nodes/side, $\delta=0.05$")
# ax3=ax.plot(pdX3c,pdZ3c,ls="None", marker="v",markevery=(0,5),label=r"100 nodes, h=0.05")
# ax4=ax.plot(pdX4c,pdZ4c,ls="None", marker="s",markevery=(0,8),label=r"160 nodes, h=0.05")
# ax4=ax.plot(pdX3c,pdZ3c,ls="None", marker="o",markevery=(4,6),label="200 nodes, h=0.020")
# ax = fig.add_subplot(211, projection='3d')
# ax.plot(analyticalX1,analyticalY1,analyticalZ1,ls="None", marker="o",label="Analytical")
# plt.title('Simply Supported Plate Slice')

plt.legend(loc=9, borderaxespad=0.)

ax.set_xlabel('Distance Along Plate Centerline')
ax.set_xticks(np.linspace(0.0,1.0,num=5))
ax.set_ylabel('Deflection under Uniform Pressure')
ax.set_yticks(1.0e-5*np.linspace(0.0,-5,num=6))
ax.grid(True)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

if saving:
    fig.savefig("../elasticPlate_convergence_dx.pgf")
plt.show()



