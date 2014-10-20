#!/usr/bin/env python

saving = False

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

figureWidth = 6.0
fig=plt.figure(1,figsize=(figureWidth,figureWidth*1.5))
fig.suptitle('Double Torsion Fracture Test',fontsize=16)

pdNameList=["./DoubleTorsionTest6_n101_h03/DoubleTorsionTest6_n101_h03_1_exp_58.npz", 
    "./DoubleTorsionTest6_n101_h03/DoubleTorsionTest6_n101_h03_2_exp_52.npz", 
    "./DoubleTorsionTest6_n101_h03/DoubleTorsionTest6_n101_h03_3_exp_50.npz", 
    "./DoubleTorsionTest6_n101_h03/DoubleTorsionTest6_n101_h03_4_exp_89.npz"]

pdTitleList=['Displacement = 0.010','Displacement = 0.012','Displacement = 0.015','Displacement = 0.020','Displacement = 0.030']

def decimalForm1(x,pos):
#     if x<0.001:return '%2.0f' % x
    if x<0.001:return ' '
    return '%1.1f' % x

def decimalForm2(x,pos):
    return '%1.2f' % x

x3Dformatter = FuncFormatter(decimalForm1)
z3Dformatter = FuncFormatter(decimalForm2)

numplots = len(pdNameList)
for index in range(numplots):
    PDfile1name = pdNameList[index]
    PDdata1 = np.load(PDfile1name)
    ux1 = PDdata1['ux']
    uy1 = PDdata1['uy']
    uz1 = PDdata1['uz']
    x01 = PDdata1['x0']
    y01 = PDdata1['y0']
    nodeHealth1 = PDdata1['nodeHealth']
    damage1 = 1.0-nodeHealth1

    xdim = 201
    ydim = 101
    numpts = xdim*ydim
    pdx01_2D = np.reshape(x01[:numpts],(xdim,ydim))
    pdy01_2D = np.reshape(y01[:numpts],(xdim,ydim))
    pdZ_2D = np.reshape(uz1[:numpts],(xdim,ydim))
    pdDamage_2D = np.reshape(damage1[:numpts],(xdim,ydim))
    
    # Displacement Subplot
    ax2=fig.add_subplot(numplots,2,2*index+1, projection='3d', aspect=1.0)
    im2 = ax2.plot_surface(pdx01_2D,pdy01_2D,pdZ_2D,  rstride=10, cstride=10, cmap=plt.cm.rainbow,vmin=-0.03, vmax=0.01)

    ax2.xaxis.set_major_locator(LinearLocator(numticks=3))
    ax2.xaxis.set_major_formatter(x3Dformatter)
    ax2.yaxis.set_major_locator(LinearLocator(numticks=3))
    ax2.yaxis.set_major_formatter(x3Dformatter)
    ax2.zaxis.set_major_locator(LinearLocator(numticks=0))
    ax2.zaxis.set_major_formatter(z3Dformatter)
    ax2.azim = -120
    ax2.elev = 20
    ax2.auto_scale_xyz([0.0, 2.0], [0.0, 1.0], [-0.03, 0.0])
    
    # Damage subplot
    ax1= fig.add_subplot(numplots,2,2*index+2,adjustable='box', aspect=1.0)
    im = ax1.contourf(pdx01_2D,pdy01_2D,pdDamage_2D,levels = [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1])

    ax1.set_title(pdTitleList[index],fontsize=13)
    ax1.yaxis.tick_right()

fig.subplots_adjust(left=0.18, top = 0.92, bottom=0.05,right=0.8, wspace=0.1, hspace=0.12)
# fig.subplots_adjust(left=None, bottom=None, right=0.5, wspace=None, hspace=None)
cbar_ax1 = fig.add_axes([0.88, 0.05, 0.05, 0.87])
cbar_ax2 = fig.add_axes([0.10, 0.05, 0.05, 0.87])
fig.text(0.96, 0.48, 'Damage', ha='center', va='center', rotation='vertical',fontsize = 16)
bar1=fig.colorbar(im, cax=cbar_ax1)
bar2=fig.colorbar(im2, cax=cbar_ax2)
bar2.set_ticks([-.03,-.025,-0.02,-0.015,-0.005,0.0,0.005,0.01])

bar2.ax.yaxis.set_ticks_position('left')
fig.text(0.05, 0.48, 'Displacement', ha='center', va='center', rotation='vertical',fontsize = 16)
if saving:
    make_sure_path_exists("./writeup/plots")
    fig.savefig("./writeup/plots/DoubleTorsionDD.pgf")
plt.show()



