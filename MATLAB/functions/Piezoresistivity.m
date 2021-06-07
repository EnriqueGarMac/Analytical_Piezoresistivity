function [sigma_EFF_serie,strain_vector,Drho_11,Drho_12,L11_tract,L12_tract,L11_comp,L12_comp,L44_tract,L44_comp,fc,Xi] = Piezoresistivity(dco,Lambdao,L_CNT,d_CNT,sigma_iter,sigma_M,densm,densp,vio,str_comp,str_tens)


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
% Volume fraction
vio=densm./(densm+(100./vio-1)*densp);  % Transformation to volume fraction

% Range of deformations
strain_vector=[0,linspace(str_comp,str_tens,699)/100]';

% Initialize variables
Drho_12=zeros(length(strain_vector),1);
Drho_11=Drho_12;
Xi = zeros(1,length(strain_vector));
fc = zeros(1,length(strain_vector));

sigma_EFF_serie = cell(length(strain_vector));
for j=1:length(strain_vector)
    
    % Uni-axial stretching
    % ====================
    strain=[0,0,strain_vector(j)]; % Constrained lateral displacement
    strainvol=1+strain;
    % Stretching induced volume expansion
    vi=vio/(strainvol(1)*strainvol(2)*strainvol(3));
    
    %% PERCOLATION THRESHOLD
    s=L_CNT/d_CNT;
    I = 1/(1.0187+0.25457*strainvol(3)-0.25461*log(strainvol(3)));
    fc(j) = pi/(5.77*s*I);
    %% 1. INTERPHASE
    [Sigma_int_EH,t_EH,Sigma_int_CN,t_CN]=interphase_CNT(CNT_prop,vi,fc(j),dco,Lambdao);
    Sigma_int=[Sigma_int_EH,Sigma_int_CN];
    t=[t_EH,t_CN];
    %% 2. EQUIVALENT CYLINDER
    [sigmaT_EH,sigmaL_EH,sigmaT_CN,sigmaL_CN]=equivalent_filler(sigmaT_CNT,sigmaL_CNT,Sigma_int,L_CNT,t,d_CNT);
    equi_filler=[sigmaT_EH,sigmaL_EH,sigmaT_CN,sigmaL_CN];
    %% 3. MICROMECHANICS PIEZORESISTIVE CNT
    [sigma_EFF,Xi(j)]=micro_piezoCNT_cf(equi_filler,vi,CNT_prop,sigma_M,fc(j),t,strain);
    % Xi/Xi0
    sigma_EFF_serie(j) = {sigma_EFF};
    if j==1
        sigma_EFFo=sigma_EFF(2,2);
    end
    Drho_12(j)=(sigma_EFFo/sigma_EFF(1,1))-1;
    Drho_11(j)=(sigma_EFFo/sigma_EFF(3,3))-1;
    
end



%% Characterization of the strain-sensing curves

% L11
% ---------------------------------------
sensitivity = Drho_11(2:end)';
strainserie = strain_vector(2:end)';
% Compression
poscompress=find(strainserie>=0,1)-1;
x=-flip(strainserie(2:poscompress));
y=-flip(sensitivity(2:poscompress));
[L11_comp,~,~]=gauge_reg(x,y);
% Traction
x=strainserie(poscompress+1:end);
y=sensitivity(poscompress+1:end);
[L11_tract,~,~]=gauge_reg(x,y);
        
% L12
% ---------------------------------------
sensitivity = Drho_12(2:end)';
strainserie = strain_vector(2:end)';
% Compression
poscompress=find(strainserie>=0,1)-1;
x=-flip(strainserie(1:poscompress));
y=-flip(sensitivity(1:poscompress));
[L12_comp,~,~]=gauge_reg(x,y);
% Traction
x=strainserie(poscompress+1:end);
y=sensitivity(poscompress+1:end);
[L12_tract,~,~]=gauge_reg(x,y);

% L44
L44_tract = (L11_tract-L12_tract)/2;
L44_comp = (L11_comp-L12_comp)/2; 


% Output
Xi(1) = [];
fc(1) = [];
sigma_EFF_serie(1) = [];
Drho_12(1) = [];
Drho_11(1) = [];
strain_vector(1) = [];
end


