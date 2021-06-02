# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:32:50 2021

@author: Enrique GM
"""
import numpy as np
import math

def Eff_conductividy(dco,Lambdao,L_CNT,d_CNTo,sigma_iter,sigma_M,densm,densp,vio):

    # Properties of CNTs
    # ==================
    # Length
    L_CNT=L_CNT*10**(-6);
    # Diameter
    d_CNT=d_CNTo*10**(-9);
    # Conductivity of CNTs (L=longitudinal, T=transversal)
    sigmaL_CNT=10**sigma_iter;
    sigmaT_CNT=10**sigma_iter;
    CNT_prop=[d_CNT,L_CNT];
    
    # MICROMECHANICS MODELLING
    # ==========================
    # PERCOLATION THRESHOLD
    s=L_CNT/d_CNT;
    I = 1/(1.0187);
    fc = np.pi/(5.77*s*I);
    # Volume fraction
    vi=densm/(densm+(100./vio-1)*densp);  # Transformation to volume fraction
    # 1. INTERPHASE
    [Sigma_int_EH,t_EH,Sigma_int_CN,t_CN]=interphase_CNT(CNT_prop,vi,fc,dco,Lambdao);
    Sigma_int=np.array([Sigma_int_EH,Sigma_int_CN]);
    t=np.array([t_EH,t_CN]);
    # 2. EQUIVALENT CYLINDER
    [sigmaT_EH,sigmaL_EH,sigmaT_CN,sigmaL_CN]=equivalent_filler(sigmaT_CNT,sigmaL_CNT,Sigma_int,L_CNT,t,d_CNT);
    equi_filler=[sigmaT_EH,sigmaL_EH,sigmaT_CN,sigmaL_CN];
    # 3. MICROMECHANICS PIEZOELECTRIC CNT
    [sigma_EFF,Xi]=micro_piezoCNT_cf(equi_filler,vi,CNT_prop,sigma_M,fc,t,[0,0,0]);
    return sigma_EFF


def interphase_CNT(CNT_prop,f,fc,dco,Lambdao):

    d_CNT=CNT_prop[0];
    L_CNT=CNT_prop[1];
    rc=d_CNT/2.;
    
    # Assumptions
    # =================
    # Maximum possible distance that allows the tunneling penetration of
    # electrons
    dc = dco*10**(-9);
    # Planck constant
    hplanck = 6.626068*10**(-34);
    # Mass of an electron
    m = 9.10938291*10**(-31);
    #% Electric charge of an electron
    ee = 1.602176565*10**(-19);
    # Potential barrier height
    Lambda=Lambdao*ee;
    
    # Initial calculations
    # ==================
    # Aspect ratio
    asp=L_CNT/d_CNT;
    # Contact area of CNTs
    a_EH=np.pi*(d_CNT/2)**2;
    a_CN=np.pi*(d_CNT/2)**2;    
    
    # Percentage of percolated CNTs *)
    Xi = (f**(1./3.)-fc**(1./3.))/(1-fc**(1./3.));
    
    
    # Interphase
    # ==================
    # CONDUCTIVE NETWORK:
    da=(fc/f)**(1./3.)*dc;
    # Tunneling-type contact resistance between two CNTs
    Rint_CN = (da*hplanck**2./(a_CN*ee**2.*(2.*m*Lambda)**0.5))*np.exp((4.*np.pi*da/hplanck)*(2.*m*Lambda)**0.5);
    # Thickness of the interphase *)
    t_CN = da/2.;    # Power law relation after percolation
    # Conductivity of the interphase
    Sigma_int_CN = da/(a_CN*Rint_CN);
    
    # ELECTRON HOPPING:
    # Tunneling-type contact resistance between two CNTs
    Rint_EH = (dc*hplanck**2./(a_EH*ee**2.*(2.*m*Lambda)**0.5))*np.exp((4.*np.pi*dc/hplanck)*(2.*m*Lambda)**0.5);
    # Thickness of the interphase *)
    t_EH = dc/2.;    # Constant distance before percolation
    # Conductivity of the interphase
    Sigma_int_EH = dc/(a_EH*Rint_EH);
    
    
    if Xi>=0:
        Sigma_int_EH=Sigma_int_CN;
        t_EH=t_CN;

    
    
    return [Sigma_int_EH,t_EH,Sigma_int_CN,t_CN]



def equivalent_filler(sigmaT_CNT,sigmaL_CNT,Sigma_int,L,t,d_CNT):

    # Radio of the CNT
    rc=d_CNT/2;
    
    # Electron hopping
    # ================
    sigmaT_EH=(Sigma_int[0]/(L+2.*t[0]))*(L*(2.*rc**2*sigmaT_CNT+(sigmaT_CNT+Sigma_int[0])*(t[0]**2.+2.*rc*t[0]))/(2*rc**2*Sigma_int[0]+(sigmaT_CNT+Sigma_int[0])*(t[0]**2.+2.*rc*t[0]))+2.*t[0]);
    sigmaL_EH=(L+2.*t[0])*Sigma_int[0]*(sigmaL_CNT*rc**2.+Sigma_int[0]*(2.*rc*t[0]+t[0]**2.))/(2.*sigmaL_CNT*rc**2.*t[0]+2.*Sigma_int[0]*(2.*rc*t[0]+t[0]**2)*t[0]+Sigma_int[0]*L*(rc+t[0])**2.);
         
    # Conductive Networks
    # ================
    sigmaT_CN=(Sigma_int[1]/(L+2.*t[1]))*(L*(2.*rc**2*sigmaT_CNT+(sigmaT_CNT+Sigma_int[1])*(t[1]**2.+2.*rc*t[1]))/(2*rc**2*Sigma_int[1]+(sigmaT_CNT+Sigma_int[1])*(t[1]**2.+2.*rc*t[1]))+2.*t[1]);
    sigmaL_CN=(L+2.*t[1])*Sigma_int[1]*(sigmaL_CNT*rc**2.+Sigma_int[1]*(2.*rc*t[1]+t[1]**2.))/(2.*sigmaL_CNT*rc**2.*t[1]+2.*Sigma_int[1]*(2.*rc*t[1]+t[1]**2)*t[1]+Sigma_int[1]*L*(rc+t[1])**2.);
     
    return [sigmaT_EH,sigmaL_EH,sigmaT_CN,sigmaL_CN]



def micro_piezoCNT_cf(equi_filler,vi,CNT_prop,sigma_M,fc,t,strain):


    # CNT
    # ================================
    d=CNT_prop[0];
    L=CNT_prop[1];
    rc=d/2.;
    
    # Approach of the equivalent fiber
    # ================================
    sigmaT_EH = equi_filler[0];
    sigmaL_EH = equi_filler[1];
    sigmaT_CN = equi_filler[2];
    sigmaL_CN = equi_filler[3];
    
    # Percentage of percolated CNTs
    if vi<fc:
        Xi=0.;
    else:
        Xi = (vi**(1./3.)-fc**(1./3.))/(1.-fc**(1./3.));
    
    # ================================
    # EFFECTIVE PROPERTIES
    #  ================================
    
    # Effective volume fraction
    feff_EH = vi*(rc+t[0])**2*(L+2*t[0])/(rc**2*L);
    if Xi>=0:
        feff_CN = vi*(rc+t[1])**2.*(L+2.*t[1])/(rc**2.*L);
    
    # Construction of the conductivity tensors
    # Electrical conductivity tensor of the effective filler: Electron hopping *)
    Sigma_EH = np.array([[sigmaL_EH, 0., 0.],
        [0.,sigmaT_EH, 0.],
        [0.,0.,sigmaT_EH]]);
    # Electrical conductivity tensor of the effective filler: Conductive network
    Sigma_CN = np.array([[sigmaL_CN, 0., 0.],
        [0.,sigmaT_CN, 0.],
        [0.,0.,sigmaT_CN]]);
    # Electrical conductivity tensor of the matrix
    Sigma_M = np.array([[sigma_M, 0., 0.],
        [0.,sigma_M, 0.],
        [0.,0.,sigma_M]]);
    
    # Eshelby's tensor
    # ================================
    # Aspect ratio of the equivalent filler: Electron hopping
    Are = (L + 2.*t[0])/(2.*rc + 2.*t[0]);
    S22 = (Are)*(Are*(Are**2. - 1.)**0.5 - math.acosh(Are))/(2.*(Are**2. - 1.)**(3./2.));
    S33 = S22;
    S11 = 1. - 2.*S22;
    SEH = np.array([[S11, 0., 0.],
        [0., S22, 0.],
        [0., 0., S33]]);
    # Aspect ratio of the equivalent filler: Conductive Network
    SCN =np.array([[0., 0., 0.],
        [0.,0.5,0.],
        [0.,0,0.5]]);
    
    # Pre-Rotation of matrices
    # ================================
    Sigma_EH=np.matmul(np.matmul(rot(0.,np.pi/2.,0.),Sigma_EH),rot(0.,np.pi/2.,0.).T);
    SEH=np.matmul(np.matmul(rot(0.,np.pi/2.,0.),SEH),rot(0.,np.pi/2.,0.).T);
    Sigma_CN=np.matmul(np.matmul(rot(0.,np.pi/2.,0.),Sigma_CN),rot(0.,np.pi/2.,0.).T);
    SCN=np.matmul(np.matmul(rot(0.,np.pi/2.,0.),SCN),rot(0.,np.pi/2.,0.).T);
    
    
    # ELECTRON HOPPING
    # ================================
    # Field concentration factor
    delta=np.eye(3,3);
    TEH = (delta+(SEH*np.linalg.inv(Sigma_M))*(Sigma_EH-Sigma_M));
    AdilEH = np.linalg.inv(TEH);
    AdilEHoa = np.real(Orientational_average_closed_form(AdilEH,strain));
    
    # CONDUCTIVE NETWORKS
    # ================================
    # Field concentration factor
    T = (delta+(SCN*np.linalg.inv(Sigma_M))*(Sigma_CN-Sigma_M));
    TCN = T;
    AdilCN = np.linalg.inv(TCN);
    AdilCNa = np.real(Orientational_average_closed_form(AdilCN,strain));
    
    
    # ================================
    # EFFECTIVE PROPERTIES
    # ================================
    EHM = feff_EH*Orientational_average_closed_form((Sigma_EH-Sigma_M)*AdilEH*np.linalg.inv(((1.-feff_EH)*delta+feff_EH*AdilEHoa)),strain);
    CNM = feff_CN*Orientational_average_closed_form((Sigma_CN-Sigma_M)*AdilCN*np.linalg.inv(((1.-feff_CN)*delta+feff_CN*AdilCNa)),strain);
    Sigma_eff = Sigma_M + (1.-Xi)*EHM+Xi*CNM;
    
    
    return [np.real(Sigma_eff),Xi]


def rot(Beta,Alpha,Psi):

    # Compute Rotation tensor
    #
    # INPUT:
    # Beta -> Rotation around x1 axis
    # Alpha -> Rotation around x2 axis
    #
    # OUTPUT:
    # Q -> Rotation matrix of 3x3 tensor
    # Author: E. García-Macias
    # ------------------------------------------------------------------------
    
    orden=np.array([0,2,1]);
    
    R = np.zeros((3,3,3))
    
    R[0,:,:] = np.array([[1.,0.,0.],[0.,np.cos(Beta),np.sin(Beta)],[0.,-np.sin(Beta),np.cos(Beta)]]);
    R[1,:,:] = np.array([[np.cos(Alpha),0.,-np.sin(Alpha)],[0.,1.,0.],[np.sin(Alpha),0.,np.cos(Alpha)]]);
    R[2,:,:] = np.array([[np.cos(Psi),np.sin(Psi),0.],[-np.sin(Psi),np.cos(Psi),0.],[0.,0.,1.]]);
    
    Q = np.matmul(np.matmul(np.squeeze(R[orden[2],:,:]),np.squeeze(R[orden[1],:,:])),np.squeeze(R[orden[0],:,:]));
    
    return  Q



def Orientational_average_closed_form(Sigma,strain):

    Sigma11 = Sigma[0,0];
    Sigma33 = Sigma[2,2];
    Eps1 = strain[0]+1;
    Eps2 = strain[1]+1;
    Eps3 = strain[2]+1;
    
    SigmaPromedio11=(1./15.)*(5.*(2.*Sigma11+Sigma33)+4.*5.**(1./2.)*np.pi**2.*(\
      Sigma11+(-1.)*Sigma33)*((1j*(1./8008.))*5.**(-1./2.)*\
      Eps1*(Eps1+(-1.)*Eps2)*Eps2*(Eps1**2.*Eps2**2.)**(1./2.)*\
     Eps3**2.*(5.*(65760.+(-37329.)*Eps2+Eps1*((-37329.)+17192.*\
      Eps2))+(-40.)*(11448.+(-6521.)*Eps2+Eps1*((-6521.)+3024.*\
      Eps2))*Eps3+8.*(21860.+(-12474.)*Eps2+27.*Eps1*((-462.)+\
      215.*Eps2))*Eps3**2)*np.pi**(-1.)*(np.log((1j*(-1.))*\
      Eps1*Eps2**(-1.))+(-1.)*np.log(1j*Eps1*Eps2**(-1.)))**(\
      -1.)+(1j*(-1./8008.))*5.**(-1./2.)*Eps1*Eps2*(Eps1**2.*\
      Eps2**2.)**(1./2.)*Eps3**2.*(5.*Eps2*((-21920.)+12443.*Eps2)+\
      40.*(5480.+(-3816.)*Eps2+741.*Eps2**2.)*Eps3+(-2.)*(62215.+8.*\
      Eps2*((-7225.)+2079.*Eps2))*Eps3**2.+40.*Eps1*((-2740)+\
      7632.*Eps2+(-3631.)*Eps2**2+72.*((-53.)+14.*Eps2**2.)*Eps3+(\
      2890+9.*Eps2*((-224)+43.*Eps2))*Eps3**2)+Eps1**2.*(62215.+\
      29640.*Eps3+8.*(Eps2*((-18155.)+8316.*Eps2)+90.*(56.+(-43.)*\
      Eps2)*Eps2*Eps3+9.*((-462.)+215.*Eps2)*Eps3**2.)))*np.pi**(\
      -1.)*(np.log((1j*(-1.))*Eps1*Eps2**(-1.))+(-1.)*np.log(1j\
      *Eps1*Eps2**(-1.)))**(-1.)));
    
    
    SigmaPromedio22=(1/15)*(5.*(2.*Sigma11+Sigma33)+4.*5.**(1/2)*np.pi**2.*(\
      Sigma11+(-1)*Sigma33)*((1j*(-1/8008))*5.**(-1/2)*\
      Eps1*(Eps1+(-1)*Eps2)*Eps2*(Eps1**2.*Eps2**2)**(1/2)*\
     Eps3**2.*(5.*(65760+(-37329)*Eps2+Eps1*((-37329)+17192.*\
      Eps2))+(-40)*(11448+(-6521)*Eps2+Eps1*((-6521)+3024.*\
      Eps2))*Eps3+8.*(21860+(-12474)*Eps2+27.*Eps1*((-462)+\
      215.*Eps2))*Eps3**2)*np.pi**(-1)*(np.log((1j*(-1))*\
      Eps1*Eps2**(-1))+(-1)*np.log(1j*Eps1*Eps2**(-1)))**(\
      -1)+(1j*(-1/8008))*5.**(-1/2)*Eps1*Eps2*(Eps1**2.*\
      Eps2**2)**(1/2)*Eps3**2.*(5.*Eps2*((-21920)+12443.*Eps2)+\
      40.*(5480+(-3816)*Eps2+741.*Eps2**2)*Eps3+(-2)*(62215+8.*\
      Eps2*((-7225)+2079.*Eps2))*Eps3**2+40.*Eps1*((-2740)+\
      7632.*Eps2+(-3631)*Eps2**2+72.*((-53)+14.*Eps2**2)*Eps3+(\
      2890+9.*Eps2*((-224)+43.*Eps2))*Eps3**2)+Eps1**2.*(62215+\
      29640.*Eps3+8.*(Eps2*((-18155)+8316.*Eps2)+90.*(56+(-43)*\
      Eps2)*Eps2*Eps3+9.*((-462)+215.*Eps2)*Eps3**2)))*np.pi**(\
      -1)*(np.log((1j*(-1))*Eps1*Eps2**(-1))+(-1)*np.log(1j\
      *Eps1*Eps2**(-1)))**(-1)));
    
    
    SigmaPromedio33=(1/15)*(5.*(2.*Sigma11+Sigma33)+(1j*(-1/1001))*\
      Eps1*Eps2*(Eps1**2.*Eps2**2)**(1/2)*Eps3**2.*(5.*Eps2*((\
      -21920)+12443.*Eps2)+40.*(5480+(-3816)*Eps2+741.*Eps2**2)*\
      Eps3+(-2)*(62215+8.*Eps2*((-7225)+2079.*Eps2))*Eps3**2+\
      40.*Eps1*((-2740)+7632.*Eps2+(-3631)*Eps2**2+72.*((-53)+\
      14.*Eps2**2)*Eps3+(2890+9.*Eps2*((-224)+43.*Eps2))*\
     Eps3**2)+Eps1**2.*(62215+29640.*Eps3+8.*(Eps2*((-18155)+\
      8316.*Eps2)+90.*(56+(-43)*Eps2)*Eps2*Eps3+9.*((-462)+\
      215.*Eps2)*Eps3**2)))*np.pi*((-1)*Sigma11+Sigma33)*(np.log((\
      1j*(-1))*Eps1*Eps2**(-1))+(-1)*np.log(1j*Eps1*\
      Eps2**(-1)))**(-1));
    
    sigmaeff = np.array([[SigmaPromedio11,0.,0.],[0.,SigmaPromedio22,0.],[0.,0.,SigmaPromedio33]])
    
    return sigmaeff 
