
function Q=rot(Beta,Alpha,Psi)

% Compute Rotation tensor
%
% INPUT:
% Beta -> Rotation around x1 axis
% Alpha -> Rotation around x2 axis
%
% OUTPUT:
% Q -> Rotation matrix of 3x3 tensor
% Author: E. García-Macias
% ------------------------------------------------------------------------
opt=1;

if opt==1
orden=[1,3,2];

R = zeros(3,3,3) ;

R(1,:,:) = [1,0,0;0,cos(Beta),sin(Beta);0,-sin(Beta),cos(Beta)];
R(2,:,:) = [cos(Alpha),0,-sin(Alpha);0,1,0;sin(Alpha),0,cos(Alpha)];
R(3,:,:) = [cos(Psi),sin(Psi),0;-sin(Psi),cos(Psi),0;0,0,1];

Q = squeeze(R(orden(3),:,:))*squeeze(R(orden(2),:,:))*squeeze(R(orden(1),:,:));

else
    
Beta=Beta*180/pi;
Alpha=Alpha*180/pi;
Psi=Psi*180/pi;
orden=[1,3,2];

R = zeros(3,3,3) ;

R(1,:,:) = [1,0,0;0,cosd(Beta),sind(Beta);0,-sind(Beta),cosd(Beta)];
R(2,:,:) = [cosd(Alpha),0,-sind(Alpha);0,1,0;sind(Alpha),0,cosd(Alpha)];
R(3,:,:) = [cosd(Psi),sind(Psi),0;-sind(Psi),cosd(Psi),0;0,0,1];

Q = squeeze(R(orden(3),:,:))*squeeze(R(orden(2),:,:))*squeeze(R(orden(1),:,:));
end
% Q = [cosd(Alpha),-sind(Alpha)*sind(Beta),cosd(Beta)*sind(Alpha);0,cosd(Beta),sind(Beta);-sind(Alpha),-cosd(Alpha)*sind(Beta),cosd(Alpha)*cosd(Beta)];
end