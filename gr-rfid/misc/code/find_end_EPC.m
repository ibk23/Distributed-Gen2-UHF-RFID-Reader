function [ end_EPC_index ] = find_end_EPC( waveform, start_point_search )
%find_end_EPC Summary of this function goes here
%   Detailed explanation goes here
high_thr = 0.3255;
low_thr = 0.3225;
end_EPC_index= 0;
for i = start_point_search:start_point_search+1800
    % are_essentially_equal is a logical (a true or false value).
    are_within_range = waveform(i:i+50) > low_thr & waveform(i:i+50) < high_thr;
    if all(are_within_range)
        end_EPC_index = i;
        to_print = ['Found end of EPC at ', num2str(end_EPC_index)];
        disp(to_print);
        break
    else
        continue
    end
end
if end_EPC_index == 0
    error('Did not find end point of EPC')
end
end