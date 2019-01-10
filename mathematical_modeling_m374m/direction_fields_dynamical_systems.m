%%% Homework 4 %%%
close all
%% Pg 87 #3
clc; clear; clf;
[x,y] = meshgrid(-5:1:5, -5:1:5);

dx = y.^2;
dy = -2.*x./3;

dx = dx/norm(dx);
dy = dy/norm(dy);

quiver(x,y,dx,dy)
grid on
hold on

% x1 = -5:.1:5;
% c =  -20:2:20;
% for i = 1:length(c)
% y1 = nthroot((-x1.^2 + c(i)), 3);
% plot(x1,y1)
% end
% axis([-5,5,-5,5])
% hold off

%% Pg 87 #5
clc; clear; clf;
[x,y] = meshgrid(-6:1:6, -6:1:6);

dx = y - x;
dy = -y + (5.*x.^2)./(4+x.^2);

dx = dx/norm(dx);
dy = dy/norm(dy);

quiver(x,y,dx,dy)
grid on
axis([-6,6,-6,6])
hold on

% c = -5:5:25;
% for i=1:length(c)
%   [xsoln,ysoln]=ode45(@diff,[-50 75],c) ; 
%   plot(xsoln,ysoln,'LineWidth',1)  ; %plot y versus x
% end
% 
% function dydx = diff(x,y)
% dydx = (-y + ((5.*x.^2)./(4 + x.^2)) ).*(1./(y-x));
% end

%% Pg 93 #1(f)
clc; clear; clf;
[x,y] = meshgrid(-10:1:10, -10:1:10);

dx = -2.*x - 3.*y;
dy = 3.*x - 2.*y;

dx = dx/norm(dx);
dy = dy/norm(dy);

quiver(x,y,dx,dy)
grid on
axis([-5,5,-5,5])

% c1 = 1; c2 = 1;
% t = -10:.1:10;
% x1 = c1.*exp(-2.*t).*cos(3.*t) - c2.*exp(-2.*t).*sin(3.*t);
% y1 = c1.*exp(-2.*t).*sin(3.*t) - c2.*exp(-2.*t).*cos(3.*t);
% hold on
% plot(x1,y1)