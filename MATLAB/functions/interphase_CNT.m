function [Sigma_int_EH,t_EH,Sigma_int_CN,t_CN]=interphase_CNT(CNT_prop,f,fc,dco,Lambdao)


format long

d_CNT=CNT_prop(1);
%L_CNT=CNT_prop(2)*updated_length(strain*0,poism);
L_CNT=CNT_prop(2);
rc=d_CNT/2;

% Assumptions
% =================
% Maximum possible distance that allows the tunneling penetration of
% electrons
dc = dco*10^(-9);
% dc = 1.8*10^(-9)*updated_length(strain*0,poism)
% dc= 1.8*10^(-9);
% Planck constant
hplanck = 6.626068*10^(-34);
% Mass of an electron *)
m = 9.10938291*10^(-31);
% Electric charge of an electron
ee = 1.602176565*10^(-19);
% Potential barrier height
Lambda=Lambdao*ee;

% Initial calculations
% ==================
% Aspect ratio
asp=L_CNT/d_CNT;
% Contact area of CNTs
% a_EH=(d_CNT)^2;
a_EH=pi*(d_CNT/2)^2;
a_CN=pi*(d_CNT/2)^2;
% a_CN=(d_CNT)^2;


% Percentage of percolated CNTs *)
Xi = (f^(1/3)-fc^(1/3))/(1-fc^(1/3));


% Interphase
% ==================
% CONDUCTIVE NETWORK:
da=(fc/f)^(1/3)*dc;
% Tunneling-type contact resistance between two CNTs 
Rint_CN = (da*hplanck^2/(a_CN*ee^2*(2*m*Lambda)^0.5))*exp((4*pi*da/hplanck)*(2*m*Lambda)^0.5);
% Thickness of the interphase *)
t_CN = da/2;    %* Power law relation after percolation
% Conductivity of the interphase
Sigma_int_CN = da/(a_CN*Rint_CN);

% ELECTRON HOPPING:
% Tunneling-type contact resistance between two CNTs 
Rint_EH = (dc*hplanck^2/(a_EH*ee^2*(2*m*Lambda)^0.5))*exp((4*pi*dc/hplanck)*(2*m*Lambda)^0.5);
% Thickness of the interphase *)
t_EH = dc/2;    %* Constant distance before percolation
% Conductivity of the interphase
Sigma_int_EH = dc/(a_EH*Rint_EH);



if Xi>=0
Sigma_int_EH=Sigma_int_CN;
t_EH=t_CN;
end


end