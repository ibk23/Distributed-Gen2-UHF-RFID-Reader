%% MATLAB script to plot RFID data
% Author: Ilhaan Rasheed
% Date: October 29th 2015

clc; clear all; close all

%% Source
%fi_1 = fopen('../data/5MHz_separation','rb');
%fi_1 = fopen('../data/source','rb');
fi_1 = fopen('../data/source','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end);
x_2 = 1i*x_inter_1(2:2:end);
hold on
subplot(3,2,1)
plot(abs(x_1),'r')
hold on
plot(abs(x_2))
title('source')
xlabel('Time (us)')
ylabel('Amplitude')

%% Matched Filter
fi_1 = fopen('../data/matched_filter','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine  real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(3,2,2)
plot(abs(x_1))
title('filter')
xlabel('Time (us)')
ylabel('Amplitude')

%% Gate
fi_1 = fopen('../data/matched_filter','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

subplot(3,2,3)
plot(abs(x_1))
title('FIR filter')
xlabel('Time (us)')
ylabel('Amplitude')

%% Gate
fi_1 = fopen('../data/gate','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);
 
subplot(3,2,4)
plot(abs(x_1))
title('gate')
xlabel('Time (us)')
ylabel('Amplitude')

%% Reader
fi_1 = fopen('../data/reader_interp','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1+2:2:end) + 1i*x_inter_1(2:2:end-1);

% Since data is not complex as per reader.py, plotting x_inter_1-
subplot(3,2,5)
plot(abs(x_inter_1))
title('reader')
xlabel('Time (us)')
ylabel('Amplitude')


%% Decoder
fi_1 = fopen('../data/sink','rb');
%fi_1 = fopen('../data/reader_interp','rb');
%fi_1 = fopen('../data/sinewave','rb');
x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);



subplot(3,2,6)
plot(abs(x_1))
%title('interpolated reader')
title('sink')
xlabel('Time (us)')
ylabel('Amplitude') 



%figure()
%spectrogram(abs(x_1),'yaxis')

fi_1 = fopen('../data/source','rb');

x_inter_1 = fread(fi_1, 'float32');

% Data is complex - combine real & imaginary parts
x = x_inter_1(3.52e6:2:3.5201e6);
y = x_inter_1(3.52e6+1:2:3.5201e6+1);

%plot(x,y,'d')
%figure();
%plot(y)