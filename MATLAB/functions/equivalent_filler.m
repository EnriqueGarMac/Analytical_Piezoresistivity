function [sigmaT_EH,sigmaL_EH,sigmaT_CN,sigmaL_CN]=equivalent_filler(sigmaT_CNT,sigmaL_CNT,Sigma_int,L,t,d_CNT)


% Radio of the CNT
rc=d_CNT/2;

% Electron hopping
% ================
sigmaT_EH=(Sigma_int(1)/(L+2*t(1)))*(L*(2*rc^2*sigmaT_CNT+(sigmaT_CNT+Sigma_int(1))*(t(1)^2+2*rc*t(1)))/(2*rc^2*Sigma_int(1)+(sigmaT_CNT+Sigma_int(1))*(t(1)^2+2*rc*t(1)))+2*t(1));
sigmaL_EH=(L+2*t(1))*Sigma_int(1)*(sigmaL_CNT*rc^2+Sigma_int(1)*(2*rc*t(1)+t(1)^2))/(2*sigmaL_CNT*rc^2*t(1)+2*Sigma_int(1)*(2*rc*t(1)+t(1)^2)*t(1)+Sigma_int(1)*L*(rc+t(1))^2);
     
% Conductive Networks
% ================
sigmaT_CN=(Sigma_int(2)/(L+2*t(2)))*(L*(2*rc^2*sigmaT_CNT+(sigmaT_CNT+Sigma_int(2))*(t(2)^2+2*rc*t(2)))/(2*rc^2*Sigma_int(2)+(sigmaT_CNT+Sigma_int(2))*(t(2)^2+2*rc*t(2)))+2*t(2));
sigmaL_CN=(L+2*t(2))*Sigma_int(2)*(sigmaL_CNT*rc^2+Sigma_int(2)*(2*rc*t(2)+t(2)^2))/(2*sigmaL_CNT*rc^2*t(2)+2*Sigma_int(2)*(2*rc*t(2)+t(2)^2)*t(2)+Sigma_int(2)*L*(rc+t(2))^2);
 
end