% import data using gr-utils octave function
c = read_complex_binary('../data/source_12:05:57_070917');
% apply median filter to he data to remove noise
c_med_fil = medfilt1(abs(c),35,'truncate');
% plot result one over the other 
plot((1:200000)/2e6,abs(c(1:200000)), (1:200000)/2e6, c_med_fil(1:200000));
start_point = input('Please enter the point in time to begin looking at: ');
start_point = start_point * 2e6;
a = 0.0001;
tol = eps(a); % A very small value.
start_EPC_index = find_start_EPC(c_med_fil, tol, start_point);
end_EPC_index = start_EPC_index + 6745;