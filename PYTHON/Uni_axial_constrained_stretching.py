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
# Weight fraction
vi = 1;       # [%]

# STRAIN SENSING CURVES
# Maximum compression
str_comp = -5;  # [%]
# Maximum traction
str_tens = 5;  # [%]
[strain_vector,Drho_11,Drho_12,L11_tract,L12_tract,L11_comp,L12_comp,L44_tract,L44_comp,fc,Xi] = Piezoresistivity(dco,Lambdao,Lengthp,Diameterp,np.log10(sigma),sigma_M,densm,densp,vi,str_comp,str_tens);


fig = plt.figure(1,figsize=(18,8))
ax = plt.subplot(1,2,1)
plt.plot(strain_vector,100.*Drho_11,'-b',linewidth=2)
plt.plot(strain_vector[np.argwhere(strain_vector>=0)],100*strain_vector[np.argwhere(strain_vector>=0)]*L11_tract,'--r',linewidth=2)
plt.plot(strain_vector[np.argwhere(strain_vector<=0)],100*strain_vector[np.argwhere(strain_vector<=0)]*L11_comp,'--r',linewidth=2)
plt.ylabel(r'$\frac{\sigma_o}{\sigma_{nn}}-1$ [%]', fontsize=18)
plt.xlabel(r'Strain, $\varepsilon$', fontsize=18)
plt.title(r'Compression: $\lambda_{11} = $'+str(round(L11_tract,4))+'; $\lambda_{44} = $'+str(round(L44_tract,4))+';  Traction: $\lambda_{11} = $'+str(round(L11_comp,4))+'; $\lambda_{44} = $'+str(round(L44_comp,4)), fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=14)

ax2 = plt.subplot(1,2,2)
plt.plot(strain_vector,100.*Drho_12,'-b',linewidth=2)
plt.plot(strain_vector[np.argwhere(strain_vector>=0)],100*strain_vector[np.argwhere(strain_vector>=0)]*L12_tract,'--r',linewidth=2)
plt.plot(strain_vector[np.argwhere(strain_vector<=0)],100*strain_vector[np.argwhere(strain_vector<=0)]*L12_comp,'--r',linewidth=2)
plt.ylabel(r'$\frac{\sigma_o}{\sigma_{tt}}-1$ [%]', fontsize=18)
plt.xlabel(r'Strain, $\varepsilon$', fontsize=18)
plt.title(r'Compression: $\lambda_{12} = $'+str(round(L11_tract,4))+'; $\lambda_{44} = $'+str(round(L44_tract,4))+';  Traction: $\lambda_{12} = $'+str(round(L11_comp,4))+'; $\lambda_{44} = $'+str(round(L44_comp,4)), fontsize=12)
ax2.tick_params(axis='both', which='major', labelsize=14)
plt.tight_layout()
plt.show()




fig = plt.figure(2,figsize=(16,8))
ax = plt.subplot(1,2,1)
plt.plot(strain_vector,100.*fc,'-b',linewidth=2)
plt.ylabel(r'Percolation threshold, $fc$ [%]', fontsize=18)
plt.xlabel(r'Strain, $\varepsilon$', fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=14)
ax.ticklabel_format(useOffset=False, style='plain')

ax2 = plt.subplot(1,2,2)
plt.plot(strain_vector,Xi*100,'-b',linewidth=2)
plt.ylabel(r'Fraction of percolated CNTs, $\chi$ [%]', fontsize=18)
plt.xlabel(r'Strain, $\varepsilon$', fontsize=18)
ax2.tick_params(axis='both', which='major', labelsize=14)
plt.tight_layout()
plt.show()


print('Piezoresistivity matrix:')
print('***************************')
print('Compression:')
print(np.array([[L11_comp,L12_comp,L12_comp,0,0,0],[L12_comp,L11_comp,L12_comp,0,0,0],[L12_comp,L12_comp,L11_comp,0,0,0],[0,0,0,L44_comp,0,0],[0,0,0,0,L44_comp,0],[0,0,0,0,0,L44_comp]]))
print('\n')
print('Traction:')
print(np.array([[L11_tract,L12_tract,L12_tract,0,0,0],[L12_tract,L11_tract,L12_tract,0,0,0],[L12_tract,L12_tract,L11_tract,0,0,0],[0,0,0,L44_tract,0,0],[0,0,0,0,L44_tract,0],[0,0,0,0,0,L44_tract]]))
