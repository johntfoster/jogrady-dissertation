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

shear_mod = 3.75E8
bulk_mod = 1.0E9
nu=1.0/3.0

analyticalRange = np.linspace(-0.75,1.0,num=176)
zeroindex = np.argmin(np.absolute(analyticalRange))
print analyticalRange[zeroindex]
denomterm = analyticalRange*4.0/(plate_width**2.0)

analyticalZ = 0.0
multiplier = (24.0*(1.0-nu)*(gamma/(plate_length*plate_width))*(yieldstrain/thickness)/(np.pi**6.0))
for m in range(1,20,2):
    for n in range(1,20,2):
        denominator = (m*n*(((m/plate_length)**2.0+(n/plate_width)**2.0)**2.0 + 
            denomterm*m**2.0))
        mnterm =np.divide(np.sin(m*np.pi*0.5)*np.sin(n*np.pi*0.5),denominator)
        analyticalZ = analyticalZ+mnterm
analyticalZ = analyticalZ*multiplier

analyticalNorm=np.divide(analyticalZ,analyticalZ[zeroindex,None])

# Reference vector for uniform transverse loaded SSSS plate
# with in-plane tension/compression along short edge
# Roark & Young, p388
refRatio = [-0.75,-0.5,-0.25,0.0,0.15,0.5,1.0]
refDisp = [0.180,0.094,0.06,0.044,0.039,0.03,0.023]
normRefRatio = np.divide(refDisp,0.044)

file_name_list01 = [
"Nu33_n101_h03_compression0pt1/Nu33_n101_h03_compression0pt1_3_exp_8.npz",
"Nu33_n101_h03_compression0pt1/Nu33_n101_h03_compression0pt1_2_exp_8.npz",
"Nu33_n101_h03_compression0pt1/Nu33_n101_h03_compression0pt1_1_exp_8.npz",
"Nu33_n101_h03_g0pt1/Nu33_n101_h03_g0pt1_1_exp_2.npz",
"Nu33_n101_h03_tension0pt1/Nu33_n101_h03_tension0pt1_1_exp_10.npz",
"Nu33_n101_h03_tension0pt1/Nu33_n101_h03_tension0pt1_2_exp_10.npz",
"Nu33_n101_h03_tension0pt1/Nu33_n101_h03_tension0pt1_3_exp_10.npz"]

maxDisp01 = np.empty_like(refRatio)
for index,filename in enumerate(file_name_list01):
    data = np.load(filename)
    uz = data['uz']
    maxDisp01[index]=np.amax(np.absolute(uz))

# maxDisp01[3]=-analyticalZ

normMaxDisp01 = np.divide(maxDisp01,maxDisp01[3,None])

file_name_list1 = [
"Nu33_n101_h03_compression/Nu33_n101_h03_compression_2_exp_6.npz",
"Nu33_n101_h03_compression/Nu33_n101_h03_compression_1_exp_6.npz",
"Nu33_n101_h03_compression/Nu33_n101_h03_compression_0_exp_6.npz",
"Plate_nu33_n101_h03e/Plate_nu33_n101_h03e__exp_8.npz",
"Nu33_n101_h03_tension/Nu33_n101_h03_tension_0_exp_6.npz",
"Nu33_n101_h03_tension/Nu33_n101_h03_tension_1_exp_6.npz",
"Nu33_n101_h03_tension/Nu33_n101_h03_tension_2_exp_6.npz"]

maxDisp1 = np.empty_like(refRatio)
for index,filename in enumerate(file_name_list1):
    data = np.load(filename)
    uz = data['uz']
    maxDisp1[index]=np.amax(np.absolute(uz))

normMaxDisp1 = np.divide(maxDisp1,maxDisp1[3,None])

file_name_list10 = [
"Nu33_n101_h03_compression10/Nu33_n101_h03_compression10_2_exp_5.npz",
"Nu33_n101_h03_compression10/Nu33_n101_h03_compression10_1_exp_5.npz",
"Nu33_n101_h03_compression10/Nu33_n101_h03_compression10_0_exp_5.npz",
"Nu33_n101_h03_g10_2/Nu33_n101_h03_g10_2_1_exp_1.npz",
"Nu33_n101_h03_tension10/Nu33_n101_h03_tension10_0_exp_5.npz",
"Nu33_n101_h03_tension10/Nu33_n101_h03_tension10_1_exp_5.npz",
"Nu33_n101_h03_tension10/Nu33_n101_h03_tension10_2_exp_5.npz"]

maxDisp10 = np.empty_like(refRatio)
for index,filename in enumerate(file_name_list10):
    data = np.load(filename)
    uz = data['uz']
    maxDisp10[index]=np.amax(np.absolute(uz))

normMaxDisp10 = np.divide(maxDisp10,maxDisp10[3,None])

fig=plt.figure(1,figsize=(figureWidth,figureWidth*3.0/3.0))
plt.hold(True)
ax = fig.add_subplot(111)
# ax.plot(analyticalX1,analyticalZ1,label="Analytical")
# ref=ax.plot(refRatio,normRefRatio,ls="None", marker="o",label="Roark")
ref2=ax.plot(analyticalRange,analyticalNorm, marker="None",label="Analytical")
s01=ax.plot(refRatio,normMaxDisp01,ls="None", marker="o",label="Model")
# s1=ax.plot(refRatio,normMaxDisp1,ls="None", marker="o",label="pdPlate1") 
# s10=ax.plot(refRatio,normMaxDisp10,ls="None", marker="o",label="pdPlate10")
ax.set_yscale('log')
plt.title('Simply Supported Plate Stiffening')

plt.legend(loc=9, borderaxespad=0.)

ax.set_xlabel('Normalized Edge Tension')
ax.set_xticks(np.linspace(-1.0,1.0,num=5))
ax.set_ylabel('Normalized Max Deflection')
ax.set_yticks(np.logspace(-1.0,1.0,num=5))
ax.grid(True)

if saving:
    make_sure_path_exists("./writeup/plots")
    fig.savefig("./writeup/plots/plateStiffening.pgf")
plt.show()



