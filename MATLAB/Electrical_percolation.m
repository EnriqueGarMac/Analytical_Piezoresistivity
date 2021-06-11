

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
% Electrical conductivities of CNTs to be analysed
sigmaserie = 2:1:7;

%% ELECTRICAL PROPERTIES
np = 200;  % Number of data points in the percolation curve
vserie = linspace(0.001,5,np)/100; % Mass fractions [%]

sigma_serie = zeros(np,numel(sigmaserie));
for j = 1:numel(sigmaserie)
 ley(j) = {['$\sigma_c=10^',int2str(j),'$ [S/m]']};   
 for i = 1:numel(vserie)
   sigmaEFF = Eff_conductividy(dco,Lambdao,Lengthp,Diameterp,log10(sigmaserie(j)),sigma_M,densm,densp,100*vserie(i));
   sigma_serie(i,j) = sigmaEFF(1,1);
 end
end

figure('WindowState','maximized','Color',[1 1 1])
semilogy(vserie*100,sigma_serie,'-o','MarkerFaceColor','b','MarkerSize',2,'LineWidth',2)
xlabel('CNT mass fraction wt [\%]','interpreter','latex','FontSize',20)
ylabel('Effective electrical conductivity [S/m]','interpreter','latex','FontSize',20)
legend(ley,'interpreter','latex','FontSize',20)
axis square
