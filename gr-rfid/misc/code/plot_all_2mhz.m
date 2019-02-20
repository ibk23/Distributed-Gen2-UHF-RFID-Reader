%% MATLAB script to plot RFID data
% Author: Ilhaan Rasheed
% Date: October 29th 2015

clc; clear all; close all

%% Source
%fi_1 = fopen('../data/5MHz_separation','rb');
%fi_1 = fopen('../data/source','rb');
fi_1 = fopen('../data/2MHz_ssb_source','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
%x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(3,2,1)
plot(abs(x_inter_1))
title('source')
xlabel('Time (us)')
ylabel('Amplitude')

%% Matched Filter
fi_1 = fopen('../data/2MHz_ssb_sink','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(3,2,2)
plot(abs(x_1))
title('sink')
xlabel('Time (us)')
ylabel('Amplitude')

%% Matched Filter
fi_1 = fopen('../data/filter','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(3,2,3)
plot(abs(x_1))
title('filter')
xlabel('Time (us)')
ylabel('Amplitude')

%% Matched Filter
fi_1 = fopen('../data/lowpass','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(3,2,4)
plot(abs(x_1))
title('lowpass')
xlabel('Time (us)')
ylabel('Amplitude')
