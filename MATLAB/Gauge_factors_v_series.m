

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
% Weight fractions to be analysed
viserie = linspace(0.001,5,100);
% Electrical conductivities of CNTs to be analysed
sigmaserie = 2:1:7;

%% STRAIN SENSING CURVES
% Maximum compression
str_comp = -5;  % [%]
% Maximum traction
str_tens = 5;  % [%]

L11_tract = zeros(numel(viserie),numel(sigmaserie));
L12_tract = zeros(numel(viserie),numel(sigmaserie));
L11_comp = zeros(numel(viserie),numel(sigmaserie));
L12_comp = zeros(numel(viserie),numel(sigmaserie));
L44_tract = zeros(numel(viserie),numel(sigmaserie));
L44_comp = zeros(numel(viserie),numel(sigmaserie)); 
ley = cell(numel(sigmaserie),1);
for j = 1:numel(sigmaserie)
    sigma = 10^j;
    ley(j) = {['$\sigma_c=10^',int2str(j),'$ [S/m]']};
for i = 1:numel(viserie)
    % Volume fraction
    vi = viserie(i);       % [%]
    [sigma_EFF_serie,strain_vector,Drho_11,Drho_12,L11_tract(i,j),L12_tract(i,j),L11_comp(i,j),L12_comp(i,j),L44_tract(i,j),L44_comp(i,j),fc,Xi] = Piezoresistivity(dco,Lambdao,Lengthp,Diameterp,log10(sigma),sigma_M,densm,densp,vi,str_comp,str_tens);
end
end

%% REPRESENTATION

figure('WindowState','maximized','Color',[1 1 1])
colors = [1,0,0;0,1,0;0,0,0;0,0,1;0.2,0.2,0.2;0.6,0.2,0.4];
subplot(2,2,1)
hold on
for j = 1:numel(sigmaserie)
   plot(viserie,L11_tract(:,j),'-','LineWidth',2,'Color',colors(j,:))
end
hold off
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
   plot(viserie,L11_comp(:,j),'-','LineWidth',2,'Color',colors(j,:))
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




