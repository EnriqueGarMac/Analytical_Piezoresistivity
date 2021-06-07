

clear
clc

addpath(genpath('functions'));


%% INPUT PARAMETERS

% Matrix phase [Isotropic material]
densm = 1.12;               % Density g/cm3
sigma_M = 1.036000000000000e-10;        % Electrical conductivity S/m

% MWCNTs [Transverse isotropic material]
% Mechanical properties
densp = 1.392586934259224;                % Density g/cm3 
Lengthp = 3.274156450863868;                 % Length [microns] 
Diameterp = 10.146756608931748;              % Diameter [nm] 
% Electrical properties
dco = 1.870116073238336;     % Interparticle distance [nm]
Lambdao = 0.500004882406769; % Height of the potential barrier [eV]
sigma=10^7;                  % Electrical conductivity [S/m]
% Volume fraction
vi = 1;       % [%]


%% STRAIN SENSING CURVES
% Maximum compression
str_comp = -5;  % [%]
% Maximum traction
str_tens = 5;  % [%]
[sigma_EFF_serie,strain_vector,Drho_11,Drho_12,L11_tract,L12_tract,L11_comp,L12_comp,L44_tract,L44_comp,fc,Xi] = Piezoresistivity(dco,Lambdao,Lengthp,Diameterp,log10(sigma),sigma_M,densm,densp,vi,str_comp,str_tens);

%% REPRESENTATION

figure('WindowState','maximized','Color',[1 1 1])
subplot(1,2,1)
hold on
plot(strain_vector,100*Drho_11,'-b','LineWidth',2)
plot(strain_vector(strain_vector>=0),100*strain_vector(strain_vector>=0)*L11_tract,'--r','LineWidth',2)
plot(strain_vector(strain_vector<=0),100*strain_vector(strain_vector<=0)*L11_comp,'--r','LineWidth',2)
hold off
ylabel('$\frac{\sigma_o}{\sigma_{nn}}-1$ [\%]','interpreter','latex','FontSize',20)
xlabel('Strain, $\varepsilon$','interpreter','latex','FontSize',20)
title(['\textbf{Compression}: $\lambda_{11} = $',num2str(L11_tract),'; $\lambda_{44} = $',num2str(L44_tract),';  \textbf{Traction}: $\lambda_{11} = $',num2str(L11_comp),'; $\lambda_{44} = $',num2str(L44_comp)],'interpreter','latex','FontSize',15)
box on
axis square
subplot(1,2,2)
hold on
plot(strain_vector,100*Drho_12,'-b','LineWidth',2)
plot(strain_vector(strain_vector>=0),100*strain_vector(strain_vector>=0)*L12_tract,'--r','LineWidth',2)
plot(strain_vector(strain_vector<=0),100*strain_vector(strain_vector<=0)*L12_comp,'--r','LineWidth',2)
hold off
ylabel('$\frac{\sigma_o}{\sigma_{tt}}-1$ [\%]','interpreter','latex','FontSize',20)
xlabel('Strain, $\varepsilon$','interpreter','latex','FontSize',20)
title(['\textbf{Compression}: $\lambda_{11} = $',num2str(L12_tract),'; $\lambda_{44} = $',num2str(L44_tract),';  \textbf{Traction}: $\lambda_{11} = $',num2str(L12_comp),'; $\lambda_{44} = $',num2str(L44_comp)],'interpreter','latex','FontSize',15)
box on
axis square

figure('WindowState','maximized','Color',[1 1 1])
subplot(1,2,1)
plot(strain_vector,fc,'-b','LineWidth',2)
ylabel('$\frac{\sigma_o}{\sigma_{nn}}-1$ [\%]','interpreter','latex','FontSize',20)
xlabel('Strain, $\varepsilon$','interpreter','latex','FontSize',20)
title(['\textbf{Compression}: $\lambda_{11} = $',num2str(L11_tract),'; $\lambda_{44} = $',num2str(L44_tract),';  \textbf{Traction}: $\lambda_{11} = $',num2str(L11_comp),'; $\lambda_{44} = $',num2str(L44_comp)],'interpreter','latex','FontSize',15)
box on
axis square
subplot(1,2,2)
plot(strain_vector,Xi,'-b','LineWidth',2)
ylabel('$\frac{\sigma_o}{\sigma_{tt}}-1$ [\%]','interpreter','latex','FontSize',20)
xlabel('Strain, $\varepsilon$','interpreter','latex','FontSize',20)
title(['\textbf{Compression}: $\lambda_{11} = $',num2str(L12_tract),'; $\lambda_{44} = $',num2str(L44_tract),';  \textbf{Traction}: $\lambda_{11} = $',num2str(L12_comp),'; $\lambda_{44} = $',num2str(L44_comp)],'interpreter','latex','FontSize',15)
box on
axis square


disp('Piezoresistivity matrix:')
disp('**************************')
disp('Compression:')
disp([L11_comp,L12_comp,L12_comp,0,0,0;L12_comp,L11_comp,L12_comp,0,0,0;L12_comp,L12_comp,L11_comp,0,0,0;0,0,0,L44_comp,0,0;0,0,0,0,L44_comp,0;0,0,0,0,0,L44_comp])
disp(' ')
disp('Traction:')
disp('Piezoresistivity matrix:')
disp([L11_tract,L12_tract,L12_tract,0,0,0;L12_tract,L11_tract,L12_tract,0,0,0;L12_tract,L12_tract,L11_tract,0,0,0;0,0,0,L44_tract,0,0;0,0,0,0,L44_tract,0;0,0,0,0,0,L44_tract])
