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
# Weight fractions to be analysed
viserie = np.linspace(0.001,5,10,endpoint=True);
# Electrical conductivities of CNTs to be analysed
sigmaserie = np.arange(2,7+1,1);

# STRAIN SENSING CURVES
# Maximum compression
str_comp = -5;  # [%]
# Maximum traction
str_tens = 5;  # [%]

L11_tract = np.zeros((len(viserie),len(sigmaserie)));
L12_tract = np.zeros((len(viserie),len(sigmaserie)));
L11_comp = np.zeros((len(viserie),len(sigmaserie)));
L12_comp = np.zeros((len(viserie),len(sigmaserie)));
L44_tract = np.zeros((len(viserie),len(sigmaserie)));
L44_comp = np.zeros((len(viserie),len(sigmaserie))); 

for j in np.arange(0,len(sigmaserie),1):
    sigma = 10.**j;
    for i in np.arange(0,len(viserie),1):
      # Volume fraction
      vi = viserie[i];       # [%]
      [strain_vector,Drho_11,Drho_12,L11_tract[i,j],L12_tract[i,j],L11_comp[i,j],L12_comp[i,j],L44_tract[i,j],L44_comp[i,j],fc,Xi] = Piezoresistivity(dco,Lambdao,Lengthp,Diameterp,np.log10(sigma),sigma_M,densm,densp,vi,str_comp,str_tens);


# REPRESENTATION

fig = plt.figure(1,figsize=(18,8))
colors = np.array([[1,0,0;0,1,0],[0,0,0;0,0,1],[0.2,0.2,0.2],[0.6,0.2,0.4]])
subplot(2,2,1)
hold on
for j in np.arange(0,len(sigmaserie),1):
   plt.plot(viserie,L11_tract[:,j],'-',Linewidth=2,'Color',colors(j,:))

legend(ley,'interpreter','latex','FontSize',20)
ylabel('Traction: $\lambda_{11}$','interpreter','latex','FontSize',20)
xlabel('CNT volume fraction, $f_{CNT} [\%]$','interpreter','latex','FontSize',20)
box on

subplot(2,2,2)
hold on
for j = 1:numel(sigmaserie)
   plot(viserie,L12_tract(:,j),'-','LineWidth',2,'Color',colors(j,:))
end
hold off
legend(ley,'interpreter','latex','FontSize',20)
ylabel('Traction: $\lambda_{12}$','interpreter','latex','FontSize',20)
xlabel('CNT volume fraction, $f_{CNT} [\%]$','interpreter','latex','FontSize',20)
box on

subplot(2,2,3)
hold on
for j = 1:numel(sigmaserie)
   plot(viserie,L11_tract(:,j),'-','LineWidth',2,'Color',colors(j,:))
end
hold off
legend(ley,'interpreter','latex','FontSize',20)
ylabel('Compression: $\lambda_{11}$','interpreter','latex','FontSize',20)
xlabel('CNT volume fraction, $f_{CNT} [\%]$','interpreter','latex','FontSize',20)
box on

subplot(2,2,4)
hold on
for j = 1:numel(sigmaserie)
   plot(viserie,L12_comp(:,j),'-','LineWidth',2,'Color',colors(j,:))
end
hold off
legend(ley,'interpreter','latex','FontSize',20)
ylabel('Compression: $\lambda_{12}$','interpreter','latex','FontSize',20)
xlabel('CNT volume fraction, $f_{CNT} [\%]$','interpreter','latex','FontSize',20)
box on




