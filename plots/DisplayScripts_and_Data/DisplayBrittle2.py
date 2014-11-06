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
PDfile1name = "./3Pt_Brittle_d0001_h10_n200/3Pt_Brittle_d0001_h10_n200_24_brittle_1.npz"
PDlabel1 = "200 nodes, initial failure"
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
PDfile2name = "./3Pt_Brittle_d0001_h10_n200/3Pt_Brittle_d0001_h10_n200_24_brittle_3.npz"
PDlabel2 = "200 nodes"
PDdata2 = np.load(PDfile2name)
ux2 = PDdata2['ux']
uz2 = PDdata2['uz']
health2 = PDdata2['nodeHealth']
pdX2 = ma.masked_outside(ux2,0.0,plate_length)
analyticalX2 = pdX2
pdZ2 = ma.masked_array(uz2,mask=pdX2.mask)
pdHealth2 = ma.masked_array(health2,mask=pdX2.mask)

#Load third PD beam data
pdHorizon3 = 0.05
PDfile3name = "./3Pt_Brittle_d0001_h10_n200/3Pt_Brittle_d0001_h10_n200_24_brittle_5.npz"
PDlabel3 = "200 nodes, horizon 0.10"
PDdata3 = np.load(PDfile3name)
ux3 = PDdata3['ux']
uz3 = PDdata3['uz']
health3 = PDdata3['nodeHealth']
pdX3 = ma.masked_outside(ux3,0.0,plate_length)
analyticalX3 = pdX3
pdZ3 = ma.masked_array(uz3,mask=pdX3.mask)
pdHealth3 = ma.masked_array(health3,mask=pdX3.mask)

#Load fourth PD beam data
pdHorizon4 = 0.05
PDfile4name = "./3Pt_Brittle_d0001_h10_n200/3Pt_Brittle_d0001_h10_n200_24_brittle_15.npz"
PDlabel4 = "200 nodes, horizon 0.10"
PDdata4 = np.load(PDfile4name)
ux4 = PDdata4['ux']
uz4 = PDdata4['uz']
health4 = PDdata4['nodeHealth']
pdX4 = ma.masked_outside(ux4,0.0,plate_length)
analyticalX4 = pdX4
pdZ4 = ma.masked_array(uz4,mask=pdX4.mask)
pdHealth4 = ma.masked_array(health4,mask=pdX4.mask)


fig=plt.figure(1,figsize=(figureWidth,figureWidth*3.0/3.0))

ax1a=fig.add_subplot(411)
d1=ax1a.plot(pdX1,pdZ1,'b--',label='Deflection')
ax1a.set_xticks([], minor=False)
ax1a.set_xticks(np.linspace(0.0,2.0,num=5), minor=True)
ax1a.xaxis.grid(True,which='minor')
ax1a.yaxis.grid(True, which='major')
ax1a.set_yticks(1.0e-5*np.linspace(0.0,-8,num=5))
ax1a.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

ax1b=ax1a.twinx()
ax1b.set_ylim((0.0,1.0))
ax1b.yaxis.tick_right()
ax1b.set_yticks(np.linspace(0.0,1.0,num=5))
# ax1b.set_title('Node Health')
h1=ax1b.plot(pdX1,pdHealth1,'r',label='Node Health')

ax1=d1+h1
a1labs = [l.get_label() for l in ax1]
plt.legend(ax1,a1labs,bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=2, mode="expand", borderaxespad=0.)

# fig.suptitle("Single Loadstep Brittle Failure Progression",y=1.0,fontsize=14)


ax2a=fig.add_subplot(412)
ax2a.plot(pdX2,pdZ2,'b--')#,label=PDlabel2,marker=">",markevery=(5,20))
ax2a.set_xticks([], minor=False)
ax2a.set_xticks(np.linspace(0.0,2.0,num=5), minor=True)
ax2a.xaxis.grid(True,which='minor')
ax2a.yaxis.grid(True, which='major')
ax2a.set_yticks(1.0e-5*np.linspace(0.0,-8,num=5))
ax2a.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

ax2b=ax2a.twinx()
ax2b.set_ylim((0.0,1.0))
ax2b.yaxis.set_label_position("right")
ax2b.yaxis.tick_right()
ax2b.set_yticks(np.linspace(0.0,1.0,num=5))
ax2b.plot(pdX2,pdHealth2,'r')

ax3a=fig.add_subplot(413)
ax3a.plot(pdX3,pdZ3,'b--')#,label=PDlabel3,marker="v",markevery=(30,50))
ax3a.set_xticks([], minor=False)
ax3a.set_xticks(np.linspace(0.0,2.0,num=5), minor=True)
ax3a.xaxis.grid(True,which='minor')
ax3a.yaxis.grid(True, which='major')
ax3a.set_yticks(1.0e-5*np.linspace(0.0,-8,num=5))
ax3a.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

ax3b=ax3a.twinx()
ax3b.set_ylim((0.0,1.0))
ax3b.yaxis.set_label_position("right")
ax3b.yaxis.tick_right()
ax3b.set_yticks(np.linspace(0.0,1.0,num=5))
ax3b.plot(pdX3,pdHealth3,'r')

ax4a=fig.add_subplot(414)
ax4a.plot(pdX4,pdZ4,'b--')#,label=PDlabel3,marker="v",markevery=(30,50))
ax4a.set_xlabel('Distance along Beam')
ax4a.set_xticks(np.linspace(0.0,2.0,num=5))
ax4a.xaxis.grid(True,which='major')
ax4a.yaxis.grid(True, which='major')
ax4a.set_yticks(1.0e-5*np.linspace(0.0,-8,num=5))
ax4a.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

ax4b=ax4a.twinx()
ax4b.set_ylim((0.0,1.0))
ax4b.yaxis.set_label_position("right")
ax4b.yaxis.tick_right()
ax4b.set_yticks(np.linspace(0.0,1.0,num=5))
ax4b.plot(pdX4,pdHealth4,'r')

fig.subplots_adjust(left=0.1, bottom=None, right=0.88, wspace=None, hspace=None)

fig.text(0.03, 0.5, 'Deflection', ha='center', va='center', rotation='vertical')
fig.text(0.98, 0.5, 'Node Health', ha='center', va='center', rotation='vertical')

if saving:
    fig.savefig("../brittle_h10_n200.pgf")
plt.show()



