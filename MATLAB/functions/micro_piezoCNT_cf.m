function [Sigma_eff,Xi]=micro_piezoCNT_cf(equi_filler,vi,CNT_prop,sigma_M,fc,t,strain)

format long

% CNT
% ================================
d=CNT_prop(1);
%L=CNT_prop(2)*updated_length(strain,poism);
L=CNT_prop(2);
rc=d/2;

% Approach of the equivalent fiber
% ================================
sigmaT_EH = equi_filler(1);
sigmaL_EH = equi_filler(2);
sigmaT_CN = equi_filler(3);
sigmaL_CN = equi_filler(4);

% Percentage of percolated CNTs *)
if vi<fc
    Xi=0;
else
    Xi = (vi^(1/3)-fc^(1/3))/(1-fc^(1/3));
end

%% ================================
% EFFECTIVE PROPERTIES
%  ================================

% Effective volume fraction
feff_EH = vi*(rc+t(1))^2*(L+2*t(1))/(rc^2*L);
if Xi>=0
    feff_CN = vi*(rc+t(2))^2*(L+2*t(2))/(rc^2*L);
end


% Construction of the conductivity tensors
% Electrical conductivity tensor of the effective filler: Electron hopping *)
Sigma_EH = [sigmaL_EH, 0, 0;
    0,sigmaT_EH, 0;
    0,0,sigmaT_EH];
% Electrical conductivity tensor of the effective filler: Conductive network
Sigma_CN = [sigmaL_CN, 0, 0;
    0,sigmaT_CN, 0;
    0,0,sigmaT_CN];
% Electrical conductivity tensor of the matrix
Sigma_M =  [sigma_M, 0, 0;
    0,sigma_M, 0;
    0,0,sigma_M];
% disp('Sigma_EH')
% disp(Sigma_EH)
% Eshelby's tensor
% ================================
% Aspect ratio of the equivalent filler: Electron hopping
Are = (L + 2*t(1))/(2*rc + 2*t(1));
S22 = (Are)*(Are*(Are^2 - 1)^0.5 - acosh(Are))/(2*(Are^2 - 1)^(3/2));
S33 = S22;
S11 = 1 - 2*S22;
SEH = [S11, 0, 0;
    0, S22, 0;
    0, 0, S33];
% Aspect ratio of the equivalent filler: Conductive Network
SCN =[0, 0, 0;
    0,0.5,0;
    0,0,0.5];

% Pre-Rotation of matrices
% ================================
Sigma_EH=rot(0,pi/2,0)*Sigma_EH*rot(0,pi/2,0)';
SEH=rot(0,pi/2,0)*SEH*rot(0,pi/2,0)';
Sigma_CN=rot(0,pi/2,0)*Sigma_CN*rot(0,pi/2,0)';
SCN=rot(0,pi/2,0)*SCN*rot(0,pi/2,0)';
Sigma_M=rot(0,pi/2,0)*Sigma_M*rot(0,pi/2,0)';


% ELECTRON HOPPING
% ================================
% Field concentration factor
delta=eye(3,3);
TEH = (delta+(SEH/Sigma_M)*(Sigma_EH-Sigma_M));
AdilEH = inv(TEH);
AdilEHoa = Orientational_average_closed_form(AdilEH,strain);

% CONDUCTIVE NETWORKS
% ================================
% Field concentration factor
T = (delta+(SCN/Sigma_M)*(Sigma_CN-Sigma_M));
TCN = T;
AdilCN = inv(TCN);
AdilCNa = Orientational_average_closed_form(AdilCN,strain);


% ================================
% EFFECTIVE PROPERTIES
% ================================
EHM = feff_EH*Orientational_average_closed_form((Sigma_EH-Sigma_M)*AdilEH/((1-feff_EH)*delta+feff_EH*AdilEHoa),strain);
CNM = feff_CN*Orientational_average_closed_form((Sigma_CN-Sigma_M)*AdilCN/((1-feff_CN)*delta+feff_CN*AdilCNa),strain);
Sigma_eff = Sigma_M + (1-Xi)*EHM+Xi*CNM;


end

