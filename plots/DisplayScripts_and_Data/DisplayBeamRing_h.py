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
yieldstrain = 1.0e-3
thickness = 0.001
plate_length = 1.0
plate_width = 1.0
gamma = 0.1
eps = 1.0e-8

analyticalX1 = np.linspace(0.0,1.0,num=1001)
analyticalX2 = np.linspace(0.0,1.0,num=1001)

namebase = "./Ring_t001_n50/Ring_t001_n50_1_exp_"
# namelist = ["./Ring_t001_n100/Ring_t001_n100_1_exp_1.npz",
#     "./Ring_t001_n100/Ring_t001_n100_1_exp_4.npz",
#     "./Ring_t001_n100/Ring_t001_n100_1_exp_7.npz",
#     "./Ring_t001_n100/Ring_t001_n100_1_exp_10.npz",
#     "./Ring_t001_n100/Ring_t001_n100_1_exp_12.npz",
#     "./Ring_t001_n100/Ring_t001_n100_1_exp_6.npz"][:5]

namebase = "./BeamRing_reweight_n1280_h10_g0001pull_3/BeamRing_reweight_n1280_h10_g0001pull_3_1_exp_"
namebase = "./PlateRing_n80_h31_g0/PlateRing_n80_h31_g0_1_exp_"
namebase = "./PlateRing_n40_h31_g001push/PlateRing_n40_h31_g001push_1_exp_"
numlist = range(1,7,1)
numplots = len(numlist)

namelist = ["./BeamRing_newInt_n160_h05_g1_1_exp_88.npz",
    "./BeamRing_newInt_n320_h05_g1_1_exp_63.npz",
    "./BeamRing_newInt_n320_h10_g1_1_exp_35.npz"][1::]
labellist = [r" 160 nodes/length, $\delta=0.032$",r" 320 nodes/length, $\delta=0.016$",r" 320 nodes/length, $\delta=0.032$"][1::]
numplots = len(namelist)

#exaggerate displacement
scale=20.0
rescale=0.01
fig=plt.figure()
# plt.hold(True)

ax1 = fig.add_subplot(121,title='Exagerrated Deformation', adjustable='box', aspect=1.0)
ax2 = fig.add_subplot(122,title='X Displacement')

datanumber=0
#Load PD plate data
#     PDfile1name = namebase+str(numlist[datanumber])+".npz"
PDfile1name = namelist[datanumber]
PDlabel1 = "101x101 nodes, h10, ext10"
PDdata1 = np.load(PDfile1name)
ux1 = PDdata1['ux']
uy1 = PDdata1['uy']
uz1 = PDdata1['uz']
x01 = PDdata1['x0']
y01 = PDdata1['y0']
z01 = PDdata1['z0']

# data1mask = np.logical_or(
#     np.logical_or(0.0-eps>x01,plate_length+eps<x01),
#     np.logical_or(0.0-eps>y01,plate_width+eps<y01))
y01min = 1.2*np.min(y01)
# print y01min
data1mask = np.logical_or(0.0 > z01,y01min<y01)
pdX1 = ma.array(ux1,mask=data1mask)
pdY1 = ma.array(uy1,mask=data1mask)
pdZ1 = ma.array(uz1,mask=data1mask)

pdX1c=pdX1.compressed()
pdY1c=pdY1.compressed()
pdZ1c=pdZ1.compressed()

pdX01 = ma.array(x01,mask=data1mask)
pdY01 = ma.array(y01,mask=data1mask)
pdZ01 = ma.array(z01,mask=data1mask)
pdX01c=pdX01.compressed()
pdY01c=pdY01.compressed()
pdZ01c=pdZ01.compressed()


analyticaluX1 = np.zeros_like(pdX1c)
analyticaluY1 = np.zeros_like(pdY1c)
analyticaluZ1 = np.zeros_like(pdZ1c)

multiplier = -(gamma*(yieldstrain/thickness)
    *((plate_length/2.0)**3.0)*(9.0/64.0)/(np.pi*plate_width))

multiplier = -(gamma*(yieldstrain/thickness)
    *((plate_length/2.0)**3.0)*(1.0/8.0)/(np.pi*plate_width))

abeta = np.absolute(np.arctan2(pdZ01c,(pdX01c-(plate_length/2.0))))

analyticaluX1 = multiplier*(8.0-2.0*np.pi**2+2*np.pi*abeta+8*np.cos(abeta)
    -4*(np.pi-2*abeta)*np.sin(abeta)+np.pi*np.sin(2*abeta))

analyticaluZ1 = -multiplier*(pdZ01c/np.absolute(pdZ01c))*(3*np.pi-4*(np.pi-2*abeta)*np.cos(abeta)
    + np.pi*np.cos(2*abeta)-8*np.sin(abeta))

ax1.plot(pdX01c+scale*analyticaluX1,pdZ01c+scale*analyticaluZ1,label="Analytical")
    
ax1.plot(pdX01c+scale*pdX1c,pdZ01c+scale*pdZ1c,ls="None", marker="v",markevery=(0,20),label=labellist[datanumber])

ax2.plot(pdX01c,rescale*analyticaluX1,label="Analytical")
ax2.plot(pdX01c,rescale*pdX1c,ls="None", marker="v",markevery=(0,20),label=labellist[datanumber])
    
datanumber = 1
PDfile1name = namelist[datanumber]
PDlabel1 = "101x101 nodes, h10, ext10"
PDdata1 = np.load(PDfile1name)
ux1 = PDdata1['ux']
uy1 = PDdata1['uy']
uz1 = PDdata1['uz']
x01 = PDdata1['x0']
y01 = PDdata1['y0']
z01 = PDdata1['z0']

# data1mask = np.logical_or(
#     np.logical_or(0.0-eps>x01,plate_length+eps<x01),
#     np.logical_or(0.0-eps>y01,plate_width+eps<y01))
y01min = 1.2*np.min(y01)
# print y01min
data1mask = np.logical_or(0.0 > z01,y01min<y01)
pdX1 = ma.array(ux1,mask=data1mask)
pdY1 = ma.array(uy1,mask=data1mask)
pdZ1 = ma.array(uz1,mask=data1mask)

pdX1c=pdX1.compressed()
pdY1c=pdY1.compressed()
pdZ1c=pdZ1.compressed()

pdX01 = ma.array(x01,mask=data1mask)
pdY01 = ma.array(y01,mask=data1mask)
pdZ01 = ma.array(z01,mask=data1mask)
pdX01c=pdX01.compressed()
pdY01c=pdY01.compressed()
pdZ01c=pdZ01.compressed()


analyticaluX1 = np.zeros_like(pdX1c)
analyticaluY1 = np.zeros_like(pdY1c)
analyticaluZ1 = np.zeros_like(pdZ1c)

multiplier = -(gamma*(yieldstrain/thickness)
    *((plate_length/2.0)**3.0)*(9.0/64.0)/(np.pi*plate_width))

multiplier = -(gamma*(yieldstrain/thickness)
    *((plate_length/2.0)**3.0)*(1.0/8.0)/(np.pi*plate_width))

abeta = np.absolute(np.arctan2(pdZ01c,(pdX01c-(plate_length/2.0))))

analyticaluX1 = multiplier*(8.0-2.0*np.pi**2+2*np.pi*abeta+8*np.cos(abeta)
    -4*(np.pi-2*abeta)*np.sin(abeta)+np.pi*np.sin(2*abeta))

analyticaluZ1 = -multiplier*(pdZ01c/np.absolute(pdZ01c))*(3*np.pi-4*(np.pi-2*abeta)*np.cos(abeta)
    + np.pi*np.cos(2*abeta)-8*np.sin(abeta))
    
ax1.plot(pdX01c+scale*pdX1c,pdZ01c+scale*pdZ1c,ls="None", marker="o",markevery=(10,20),label=labellist[datanumber])

ax1.set_xlim([0,1.1])
ax1.set_xticks(np.linspace(0.0,1.0,num=5))
ax1.set_yticks(np.linspace(0.0,0.5,num=6))


ax2.plot(pdX01c,rescale*pdX1c,ls="None", marker="o",markevery=(10,20),label=labellist[datanumber])
    
ax2.yaxis.tick_right()
ax2.yaxis.set_offset_position('right')
    
ax1.legend(loc='lower center',bbox_to_anchor=(0.5,-1.2))

# plt.suptitle('Proving Ring in Tension', fontsize=16)
plt.show()

if saving:
    fig.savefig("../beamRing_h.pgf")
plt.show()

