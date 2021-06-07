function sigma_EFF=Eff_conductividy(dco,Lambdao,L_CNT,d_CNT,sigma_iter,sigma_M,densm,densp,vio)

% Properties of CNTs
% ==================
% Length
L_CNT=L_CNT*10^(-6);
% Diameter
d_CNT=d_CNT*10^(-9);
% Conductivity of CNTs (L=longitudinal, T=transversal)
sigmaL_CNT=10^sigma_iter;
sigmaT_CNT=10^sigma_iter;
CNT_prop=[d_CNT,L_CNT];

% MICROMECHANICS MODELLING
% ==========================
% PERCOLATION THRESHOLD
s=L_CNT/d_CNT;
I = 1/(1.0187);
fc = pi/(5.77*s*I);
% Volume fraction
vi=densm./(densm+(100./vio-1)*densp);  % Transformation to volume fraction
% 1. INTERPHASE
[Sigma_int_EH,t_EH,Sigma_int_CN,t_CN]=interphase_CNT(CNT_prop,vi,fc,dco,Lambdao);
Sigma_int=[Sigma_int_EH,Sigma_int_CN];
t=[t_EH,t_CN];
% 2. EQUIVALENT CYLINDER
[sigmaT_EH,sigmaL_EH,sigmaT_CN,sigmaL_CN]=equivalent_filler(sigmaT_CNT,sigmaL_CNT,Sigma_int,L_CNT,t,d_CNT);
equi_filler=[sigmaT_EH,sigmaL_EH,sigmaT_CN,sigmaL_CN];
% 3. MICROMECHANICS PIEZOELECTRIC CNT
[sigma_EFF,~]=micro_piezoCNT_cf(equi_filler,vi,CNT_prop,sigma_M,fc,t,[0,0,0]);


end