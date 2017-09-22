%% MATLAB script to plot RFID data
% Author: Ilhaan Rasheed
% Date: October 29th 2015

clc; clear all; close all

%% Source
fi_1 = fopen('../data/source','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(3,2,1)
plot(abs(x_1))
title('source')
xlabel('Time (us)')
ylabel('Amplitude')

%% Matched Filter
fi_1 = fopen('../data/matched_filter','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(3,2,2)
plot(abs(x_1))
title('matched filter')
xlabel('Time (us)')
ylabel('Amplitude')

%% Gate
fi_1 = fopen('../data/gate','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(3,2,3)
plot(abs(x_1))
title('gate')
xlabel('Time (us)')
ylabel('Amplitude')

%% Reader
fi_1 = fopen('../data/reader','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

% Since data is not complex as per reader.py, plotting x_inter_1-
subplot(3,2,4)
plot(abs(x_inter_1))
title('reader')
xlabel('Time (us)')
ylabel('Amplitude')


%% Decoder
fi_1 = fopen('../data/decoder','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(3,2,5)
plot(abs(x_1))
title('decoder')
xlabel('Time (us)')
ylabel('Amplitude') 