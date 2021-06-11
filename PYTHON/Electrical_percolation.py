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
# Electrical conductivities of CNTs to be analysed
sigmaserie = 10**np.arange(2,7+1,1);

# ELECTRICAL PROPERTIES
npp = 200;  # Number of data points in the percolation curve
vserie = np.linspace(0.001,5,npp)/100; # CNT mass fractions to be analysed [wt%]

sigma_serie = np.zeros((npp,len(sigmaserie)));
for j in np.arange(0,len(sigmaserie),1):
 for i in np.arange(1,npp+1):
   sigmaEFF = Eff_conductividy(dco,Lambdao,Lengthp,Diameterp,np.log10(sigmaserie[j]),sigma_M,densm,densp,100*vserie[i-1]);
   sigma_serie[i-1,j] = sigmaEFF[0,0];


fig, ax = plt.subplots()
for j in np.arange(0,len(sigmaserie),1):
   plt.semilogy(vserie*100,sigma_serie[:,j],'-o', label=r'$\sigma=10^'+str(int(np.log10(sigmaserie[j])))+'$')
plt.legend(fontsize=18)
plt.xlabel(r'CNT mass fraction wt [%]', fontsize=18)
plt.ylabel(r'Effective electrical conductivity [S/m]', fontsize=18)
# We change the fontsize of minor ticks label 
ax.tick_params(axis='both', which='major', labelsize=14)
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
