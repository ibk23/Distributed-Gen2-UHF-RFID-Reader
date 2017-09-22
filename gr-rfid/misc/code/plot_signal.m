clc
close all

fi_1 = fopen('../data/file_source_test','rb');
x_inter_1 = fread(fi_1, 'float32');

% if data is complex
x_1 = x_inter_1(1:2:end) + 1i*x_inter_1(2:2:end);

%plot(abs(x_1))
figure(1);
plot((1:350000)/2e6,abs(x_1(1:350000)), 'b');