#!/usr/bin/env python
# from ensight import Ensight
# VIZ_PATH='/Applications/paraview.app/Contents/MacOS/paraview'
# vector_variables = []
# scalar_variables = ['ux','uy','uz','damage','radius']
# outfile = Ensight('output', vector_variables, scalar_variables,problem.comm, viz_path=VIZ_PATH)

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
# fig.suptitle('Single Torsion Fracture',fontsize=16)
pdNameList=["./Coupled_damage_05/Coupled_damage_05_1_exp_1.npz",
#     "./Coupled_damage_05/Coupled_damage_05_1_exp_50.npz",
    "./Coupled_damage_05/Coupled_damage_05_2_exp_30.npz",
#     "./Coupled_damage_05/Coupled_damage_05_3_exp_31.npz",
    "./Coupled_damage_05/Coupled_damage_05_4_exp_35.npz",
    "./Coupled_damage_05/Coupled_damage_05_5_exp_40.npz"][:]

# pdNameList=["./DoubleTorsionTestSmall_n51_h06/DoubleTorsionTestSmall_n51_h06_1_exp_1.npz",
#     "./DoubleTorsionTestSmall_n51_h06/DoubleTorsionTestSmall_n51_h06_1_exp_2.npz"]

pdTitleList=['Initial Crack',
#     'Displacement = 0.009',
    'Displacement = 0.010',
#     'Displacement = 0.012',
    'Displacement = 0.015',
    'Displacement = 0.020',
    'Displacement = 0.030']

def decimalForm1(x,pos):
#     if x<0.001:return '%2.0f' % x
    if x<0.001:return ' '
    return '%1.1f' % x

def decimalForm2(x,pos):
    return '%1.3f' % x

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
#     ax = fig.add_subplot(numplots,1,index+1)
#     # Turn off axis lines and ticks of the big subplot
#     ax.spines['top'].set_color('none')
#     ax.spines['bottom'].set_color('none')
#     ax.spines['left'].set_color('none')
#     ax.spines['right'].set_color('none')
#     ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
    # Displacement subplot
#     ax2=fig.add_subplot(numplots,2,2*index+1, projection='3d')
    ax2=fig.add_subplot(numplots,2,2*index+1, projection='3d', aspect=1.0)
    im2 = ax2.plot_surface(pdx01_2D,pdy01_2D,pdZ_2D,  rstride=12, cstride=6, cmap=plt.cm.rainbow,vmin=-0.015, vmax=0.005)
#     ax2.set_xticks(np.linspace(0.0,2.0,num=3))
#     ax2.set_yticks(np.linspace(0.0,1.0,num=3))
#     ax2.set_zticks(np.linspace(0.0,-.03,num=4))
    ax2.set_zlim(-0.02,0.005)
    ax2.xaxis.set_major_locator(LinearLocator(numticks=3))
    ax2.xaxis.set_major_formatter(x3Dformatter)
    ax2.yaxis.set_major_locator(LinearLocator(numticks=3))
    ax2.yaxis.set_major_formatter(x3Dformatter)
    ax2.zaxis.set_major_locator(LinearLocator(numticks=0))
    ax2.zaxis.set_major_formatter(z3Dformatter)
    ax2.azim = -120
    ax2.elev = 20
#     ax2.axes.get_xaxis().set_visible(False)
#     ax2.set_axis_off()
#     ax2.auto_scale_xyz([0.0, 2.0], [0.0, 1.0], [-0.03, 0.0])
    # Damage subplot
    ax1= fig.add_subplot(numplots,2,2*index+2,adjustable='box', aspect=1.0)
    im = ax1.contourf(pdx01_2D,pdy01_2D,pdDamage_2D,levels = [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1])
    if index<(numplots-1):
        ax1.axes.get_xaxis().set_visible(False)
    ax1.set_title(pdTitleList[index],fontsize=13)
    ax1.yaxis.tick_right()

fig.subplots_adjust(left=0.18, top = 0.92, bottom=0.05,right=0.8, wspace=0.1, hspace=0.12)
# fig.subplots_adjust(left=None, bottom=None, right=0.5, wspace=None, hspace=None)
cbar_ax1 = fig.add_axes([0.88, 0.05, 0.05, 0.87])
cbar_ax2 = fig.add_axes([0.10, 0.05, 0.05, 0.87])
fig.text(0.96, 0.48, 'Damage', ha='center', va='center', rotation='vertical',fontsize = 16)
bar1=fig.colorbar(im, cax=cbar_ax1)
bar2=fig.colorbar(im2, cax=cbar_ax2)
# bar2.set_ticks([-.03,-.025,-0.02,-0.015,-0.005,0.0,0.005,0.01])
bar2.set_ticks([-0.02,-0.015,-.01,0.0,0.005,0.01])

bar2.ax.yaxis.set_ticks_position('left')
fig.text(0.05, 0.5, 'Displacement', ha='center', va='center', rotation='vertical',fontsize = 16)
if saving:
    fig.savefig("../SingleTorsion.pgf")
# fig.savefig("./writeup/plots/SingleTorsion.png")
plt.show()

# exit()
# 
# # maxdisp = np.amax(np.absolute(uz1))
# # print maxdisp
# # exit()
# 
# # #Load PD plate data
# # pdHorizon2 = 0.05
# # PDfile2name = "./2ParamPlate_SSSS_comp1_ec001_t01_nu33_n51_h05/2ParamPlate_SSSS_comp1_ec001_t01_nu33_n51_h05_exIteration_9.npz"
# # PDlabel2 = "101x101 nodes, h05, ext10"
# # PDdata2 = np.load(PDfile2name)
# # ux2 = PDdata2['ux']
# # uy2 = PDdata2['uy']
# # uz2 = PDdata2['uz']
# # x02 = PDdata2['x0']
# # y02 = PDdata2['y0']
# # 
# # data2mask = np.logical_or(
# #     np.logical_or(0.0-eps>x02,plate_length+eps<x02),
# #     np.logical_or(0.0-eps>y02,plate_width+eps<y02))
# # 
# # pdX2 = ma.array(ux2,mask=data2mask)
# # pdY2 = ma.array(uy2,mask=data2mask)
# # pdZ2 = ma.array(uz2,mask=data2mask)
# # 
# # pdX2c=pdX2.compressed()
# # pdY2c=pdY2.compressed()
# # pdZ2c=pdZ2.compressed()
# # 
# # pdX02 = ma.array(x02,mask=data2mask)
# # pdY02 = ma.array(y02,mask=data2mask)
# # pdX02c=pdX02.compressed()
# # pdY02c=pdY02.compressed()
# # 
# # #Elastic Displacement for uniform load of gamma
# # analyticalX2 = pdX02c
# # analyticalY2 = pdY02c
# # analyticalZ2 = 0.0*pdZ2c
# # multiplier = 16.0*(gamma/(plate_length*plate_width))*(yieldstrain/thickness)/(np.pi**6.0)
# # for m in range(1,10,2):
# #     for n in range(1,10,2):
# #         denominator = (m*n*((m/plate_length)**2.0+(n/plate_width)**2.0)**2.0)
# #         mnterm =(np.sin(m*np.pi*analyticalX2/plate_length)
# #             *np.sin(n*np.pi*analyticalY2/plate_width)
# #             /denominator)
# #         analyticalZ2 = analyticalZ2+mnterm
# # analyticalZ2 = analyticalZ2*multiplier
# # 
# # difference2 = pdZ2c-analyticalZ2
# # 
# # # #Load PD plate data
# # # PDfile3name = "./Plate_SSSS_Elastic_weight_1by1_ext10_n51_h10/Plate_SSSS_Elastic_weight_1by1_ext10_n51_h10_50.npz"
# # # PDlabel3 = "101x101 nodes, h025, ext10"
# # # PDdata3 = np.load(PDfile3name)
# # # ux3 = PDdata3['ux']
# # # uy3 = PDdata3['uy']
# # # uz3 = PDdata3['uz']
# # # x03 = PDdata3['x0']
# # # y03 = PDdata3['y0']
# # # 
# # # data3mask = np.logical_or(
# # #     np.logical_or(0.0-eps>x03,plate_length+eps<x03),
# # #     np.logical_or(0.0-eps>y03,plate_width+eps<y03))
# # # 
# # # pdX3 = ma.array(ux3,mask=data3mask)
# # # pdY3 = ma.array(uy3,mask=data3mask)
# # # pdZ3 = ma.array(uz3,mask=data3mask)
# # # 
# # # pdX3c=pdX3.compressed()
# # # pdY3c=pdY3.compressed()
# # # pdZ3c=pdZ3.compressed()
# # # 
# # # pdX03 = ma.array(x03,mask=data3mask)
# # # pdY03 = ma.array(y03,mask=data3mask)
# # # pdX03c=pdX03.compressed()
# # # pdY03c=pdY03.compressed()
# # # 
# # # #Elastic Displacement for uniform load of gamma
# # # analyticalX3 = pdX03c
# # # analyticalY3 = pdY03c
# # # analyticalZ3 = 0.0*pdZ3c
# # # multiplier = 16.0*(gamma/(plate_length*plate_width))*(yieldstrain/thickness)/(np.pi**6.0)
# # # for m in range(1,10,2):
# # #     for n in range(1,10,2):
# # #         denominator = (m*n*((m/plate_length)**2.0+(n/plate_width)**2.0)**2.0)
# # #         mnterm =(np.sin(m*np.pi*analyticalX3/plate_length)
# # #             *np.sin(n*np.pi*analyticalY3/plate_width)
# # #             /denominator)
# # #         analyticalZ3 = analyticalZ3+mnterm
# # # analyticalZ3 = analyticalZ3*multiplier
# # # 
# # # difference3 = pdZ3c-analyticalZ3
# # difference3 = pdZ2c-pdZ1c
# 
# fig=plt.figure()
# plt.hold(True)
# 
# # ax = fig.add_subplot(111, projection='3d')
# # ax.scatter(pdX1c,pdY1c,pdZ1c, c=pdDamage1c,cmap=plt.cm.rainbow,marker="o")
# ax = fig.add_subplot(111)
# # ax.scatter(x01,y01,c=damage1,cmap=plt.cm.rainbow)
# ax.contourf(pdx01_2D,pdy01_2D,pdDamage_2D)
# axc=ax.colorbar()
# 
# # ax.elev = 
# # ax.azim = -160
# 
# plt.title('Double Torsion Fracture Test')
# # ax.set_xlabel('x')
# # ax.set_ylabel('y')
# # ax.set_zlabel('Deflection')
# 
# 
# # ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# 
# 




