%%% Alex Gigliotti AEG2854 - Math Modeling HW 3 Problem 13 %%%
clear
close all

%% Initial variables and calculations
u = -1:0.01:7;
h = 1;
a(:,1) = 0:0.01:5;

% 'sum' represents u' from the problem
% sum = 4u(a-u) - h*exp(-u) = A - B
% A = 4u(a-u) and B = h*exp(-u) ; these are calculated using fuctions below
sum = A(a,u) - B(u,h);

%% Find Fixed Points
% Initialize variables for the loop
ustar = zeros(1,1);
a_soln = zeros(1,1);

for j = 1:length(a)
    for i = 2:length(u)

        % A Fixed Point occurs when 'sum' is zero or switches signs
        % If sign of u' goes from negative to positive, then there's a minimum or stable fixed point
        if sum(j,i-1) <= 0 && sum(j,i) >= 0
            ustar(1,j) = (u(i-1) + u(i))/2;
            a_soln(1,j) = a(j);

        % If sign of u' goes from positive to negative, then there's a maximum or unstable fixed point
        elseif sum(j,i-1) >= 0 && sum(j,i) <= 0
            ustar(2,j) = (u(i-1) + u(i))/2;
            a_soln(2,j) = a(j);
            
        end

    end
end

%% Plots
% Plot portrait of varying solutions
plot(u,sum)
grid on
axis([u(1),u(end),-10,10])
hold on
plot(u,sum.*0,'-k','LineWidth',1)
plot(u.*0,sum*2,'-k','LineWidth',1)

% Plot phase space
figure
plot(a(82:end,1),ustar(2,82:end),'-b','LineWidth',2)
hold on
plot(a(82:end,1),ustar(1,82:end),'-r','LineWidth',2)
legend('stable','unstable','Location','Northwest')
title('Bifurcation Diagram For Problem 13, Fixed h = 1')
xlabel('a')
ylabel('u^*')

function Quad = A(a,u)

Quad = 4.*u.*(a - u);

end

function Exp = B(u,h)

Exp = h.*exp(-u);

end