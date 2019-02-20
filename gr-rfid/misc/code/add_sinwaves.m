clc;    % Clear the command window.
close all;  % Close all figures (except those of imtool.)
clear;  % Erase all existing variables. Or clearvars if you want.
workspace;  % Make sure the workspace panel is showing.
format long g;
format compact;
fontSize = 20;

% Make 0.1 seconds sampled every 1/1000 of a second
t = 0 : 1/2000000 : 0.1;

% Define sine wave parameters.
f1 = 905e6; % per second
T1 = 1/f1; % period, seconds
amp1 = 1; % amplitude
f2 = 910e6; % per second
T2 = 1/f2; % period, seconds
amp2 = 1; % amplitude
f3 = 915e6; % per second
T3 = 1/f2; % period, seconds
amp3 = 1; % amplitude


% Make signals.
signal1 = amp1 * sin(2*pi*t/T1);
signal2 = amp2 * sin(2*pi*t/T2);
signal3 = amp3 * sin(2*pi*t/T3);
signal = signal1 + signal2 +signal3;
plot(t, abs(signal), 'b.-', 'LineWidth', 2, 'MarkerSize', 16);
grid on;
title('Summing 910+-5MHz sampling at 2MHz', 'FontSize', fontSize);
xlabel('Time', 'FontSize', fontSize);
ylabel('Signal', 'FontSize', fontSize);
% Make bolder x axis
line(xlim, [0,0], 'Color', 'k', 'LineWidth', 3);
legend('Sum');

