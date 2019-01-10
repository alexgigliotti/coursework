%%% Math Modeling Homework 8 %%%
%% Problem 8a
clear
close all

% Time domain
t0 = 0;
tf = 10;

% Use RK4/5 to solve system
y0 = 1; 
yp0 = 0;
ICs = [y0, yp0];
opts = odeset('RelTol',1e-03);
[tsoln, ysoln] = ode45(@F8a, [t0 tf], ICs,opts); % F8a is at the bottom of the code

% Plot Approximation
figure
t = t0:0.01:tf;
global E % Small parameter
E = 0.00001;
y = cos(t) + E.*((1/6).*sin(t) - (1/3).*sin(t));
plot(t,y,'-b','LineWidth',2)
hold on

% Plot Numerical Solution
plot(tsoln,ysoln(:,1),'--k','LineWidth',3)

% Plot formatting
xlabel('time')
ylabel('y')
title('Poincare-Linstedt Example')
legend('Analytical Solution', 'Numerical Solution (RK4)')

% System for ode45
function yp = F8a(t,y)
% yp = y' = y2
% y1 = y
% y2 = y1'
global E

yp = zeros(2,1);
yp(1) = y(2);
yp(2) = E.*y(1).*y(2).^2 - y(1);
end

