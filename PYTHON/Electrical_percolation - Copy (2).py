# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:25:51 2021

@author: Enrique GM
"""

from functions import *
import numpy as np
import matplotlib.pyplot as plt

# INPUT PARAMETERS

# Matrix phase [Isotropic material]
densm = 1.12;               # Density g/cm3
sigma_M = 1.036000000000000e-10;        # Electrical conductivity S/m

# MWCNTs [Transverse isotropic material]
# Mechanical properties
densp = 1.392586934259224;                # Density g/cm3 
Lengthp = 3.274156450863868;                 # Length [microns] 
Diameterp = 10.146756608931748;              # Diameter [nm] 
# Electrical properties
dco = 1.870116073238336;     # Interparticle distance [nm]
Lambdao = 0.500004882406769; # Height of the potential barrier [eV]
sigma=10**7;                  # Electrical conductivity [S/m]

# ELECTRICAL PROPERTIES
npp = 200;  # Number of data points in the percolation curve
vserie = np.linspace(0.001,5,npp)/100; # Weight fraction [%]

sigma_serie = np.zeros((npp,1));
for i in np.arange(1,npp+1):
   sigmaEFF = Eff_conductividy(dco,Lambdao,Lengthp,Diameterp,np.log10(sigma),sigma_M,densm,densp,100*vserie[i-1]);
   sigma_serie[i-1] = sigmaEFF[0,0];


fig, ax = plt.subplots()
plt.semilogy(vserie*100,sigma_serie,'-o')
plt.ylim([10**(-11),10**4])
plt.xlabel(r'wt [%]', fontsize=18)
plt.ylabel(r'Effective electrical conductivity [S/m]', fontsize=18)
# We change the fontsize of minor ticks label 
ax.tick_params(axis='both', which='major', labelsize=14)
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
