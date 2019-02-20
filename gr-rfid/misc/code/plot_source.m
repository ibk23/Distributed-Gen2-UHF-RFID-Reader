%% MATLAB script to plot RFID data
% Author: Ilhaan Rasheed
% Date: October 29th 2015

clc; clear all; close all

%% Source
%fi_1 = fopen('../data/5MHz_separation','rb');
%fi_1 = f0.98open('../data/source','rb');
fi_1 = fopen('../data/source','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end);
x_2 = 1i*x_inter_1(2:2:end);
hold on
subplot(1,2,1)
plot(abs(x_1),'r')
hold on
plot(abs(x_2))
title('source')
xlabel('Time (us)')
ylabel('Amplitude')

% Matched Filter
%fi_1 = fopen('../data/matched_filter','rb');

% Data is complex - combine  real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(1,2,2)
plot(abs(x_1))
title('AbsSource')
xlabel('Time (us)')
ylabel('Amplitude')

