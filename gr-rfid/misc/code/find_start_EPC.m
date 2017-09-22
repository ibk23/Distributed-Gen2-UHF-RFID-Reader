function [ EPC_index ] = find_start_EPC( waveform, tolerance, start_point_search )
%find_start_EPC finds the index position where the EPC code starts in
%waveform recorded by the source of the USRP
%   tol sets the tolerance for comparing double precision floats, used in
%   determining when the waveform is at a stable value for a window of 4
%   samples.
%   start_point_search sets the index position from which the function
%   starts to look for the EPC starting point
for i = (start_point_search):200000
    if waveform(i) < 0.310 && waveform(i) > 0.028
        value_at_start_point = zeros(4,1);
        value_at_start_point(:) = waveform(i);
        % are_essentially_equal is a logical (a true or false value).
        are_essentially_equal = ismembertol(value_at_start_point-waveform(i:i+3), zeros(4,1), tolerance);
        if all(are_essentially_equal)
            EPC_index = i;
            to_print = ['Found beginning of EPC at ', num2str(EPC_index)];
            disp(to_print);
            break
        end
    else
        continue
    end
end

end

