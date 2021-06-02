
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

orden=[1,3,2];

R = zeros(3,3,3) ;

R(1,:,:) = [1,0,0;0,cos(Beta),sin(Beta);0,-sin(Beta),cos(Beta)];
R(2,:,:) = [cos(Alpha),0,-sin(Alpha);0,1,0;sin(Alpha),0,cos(Alpha)];
R(3,:,:) = [cos(Psi),sin(Psi),0;-sin(Psi),cos(Psi),0;0,0,1];

Q = squeeze(R(orden(3),:,:))*squeeze(R(orden(2),:,:))*squeeze(R(orden(1),:,:));

end