from __future__ import print_function
import scipy
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import numpy as np
from os import getcwd

# relative_path_to_file = '../data/Corilateme/source'
relative_path_to_file = '../misc/data/gate'

Verbose=False

adc_rate = (2 * 10 ** 6)
decim = 5  # decimation of matched filter
samp_rate =  adc_rate/ decim  # Samples per second
if Verbose:
    print("Sample rate is %i = %i/%i = ADC Rate/Decim"% (samp_rate,adc_rate,decim))

half_symbol_length = int(round(12.5 * 10 ** -6 * samp_rate))
if Verbose:
    print("Half symbol length is %i"% half_symbol_length)

# Reduce computation by specifying a range to look at
first_sample = 0
last_sample = 20000
#verbose = False #Unused. Can be helpful for debugging rn16s


# Can attempt to decode RN16s in the future.
def decode_rn16(numpyarray, remove, pie):
    """Decodes the array into bits
    Arguments:
    numpyarray is an array containing the data to be processed
    remove is the number of bits at the start that should be ignored.
        common for preamble
    pie switches the mode from FM0 decoding to PIE.
        FM0 is used for tag to reader
        PIE is used for reader to tag

    Allows this function to do RN16 and ACK decoding.

    """
    # print("Plotting the rn16 i am meant to decode")
    # plt.plot(numpyarray)
    # plt.show()
    percentage_between = 50  # Should be 50, though lower value may give better results
    # Perform a weighted mean between the maximum and minimum values.
    # Due to clipping, 50% occurs quite high up, causing some false transitions.
    avg = np.average([np.amin(numpyarray), np.amax(numpyarray)], weights=[100 - percentage_between, percentage_between])
    zc = np.where(np.diff(np.sign(numpyarray - avg)))[0]
    xdiff = np.diff(zc)
    # Filter out the short duration pulses, less than 1/3 of the smallest possible pulse is definitely an error.
    # Could filter more strictly in the future, or do something clever like combining small (erroneous) pulses with
    # their neighbours so the total adds to a plausible symbol_length.
    flt_xdiff = xdiff[xdiff > (half_symbol_length / 3.0)]
    # if verbose:
    #     print("Len before and after filtering", len(xdiff), len(flt_xdiff))
    #     print("flt_xdiff IS ", flt_xdiff)
    flt_xdiff = flt_xdiff[remove:]
    # Differential decoder
    # Using Sidarth's method of counting zero crossings. Works well with high snr, but has major issues if
    # Bounce can be mistaken for a crossing.
    # Best to re-implement using Nikos' method of sampling at known times
    rn16_bits = []
    mid_read = False
    try:
        for x in np.nditer(flt_xdiff):
            if mid_read:
                mid_read = False
                continue
            if x < 1.3 * half_symbol_length:
                rn16_bits.append(0)
                mid_read = True
            else:
                rn16_bits.append(1)
                if pie:
                    mid_read = True
    except ValueError:
        return [0]

    # TODO implement more efficiently using numpy
    # position of 1s
    # print(np.where(flt_xdiff>1.3*half_symbol_length)[0])
    # print(np.diff(np.where(flt_xdiff>1.3*half_symbol_length)[0])-1)
    # if verbose:
    #     if pie:
    #         print("ACK  is ", rn16_bits, len(rn16_bits))
    #     else:
    #         print("RN16 is ", rn16_bits, len(rn16_bits))
    # Can have 17bits read, last one is false.
    if len(rn16_bits) == 17:
        rn16_bits = rn16_bits[:16]

    # if plotit:
    #     if verbose:
    #         print("Max and min are ", np.amin(numpyarray), np.amax(numpyarray))
    #     plt.axhline(y=avg, color='r', linestyle='-')
    return rn16_bits




def count_rn16s_gate(numpyarray,plot=False):
    """Find the preamble of RN16 using cross-correlation"""
    # TODO downsample for speed, if reliable enough.

    #Preamble of RN16
    sampled_signal = np.concatenate(( 1 * half_symbol_length * [-1],
2 * half_symbol_length * [1], half_symbol_length * [-1], half_symbol_length * [1],
                                     2 * half_symbol_length * [-1], half_symbol_length * [1],
                                     3 * half_symbol_length * [-5], half_symbol_length * [1]))
    # flipped = np.flipud(sampled_signal) #Usefull if convolving
    
    #normalise, since data magnitude can vary massibely.
    norm_numpyarray = numpyarray/np.amax(numpyarray)   
    #norm_numpyarray = numpyarray+0.5-np.mean(numpyarray) #instead of basing on peak value, base on average   

    #Round the numpyarray to give nice squarewaves for the correlation
    rounded = np.around(norm_numpyarray)
    #print(rounded)

    #Correlate the rounded signal with known preamble
    correlated = np.correlate(rounded - np.mean(rounded), sampled_signal)

    #Normalise the correlation for plotting on same axes
    norm_correlated =     correlated/ np.amax(correlated)
    if plot:
        plt.plot(norm_correlated)
    
    #Could use this to detect where not much signal present (i.e. noise). Should be over 24
    #unrounded_correlated = np.correlate(norm_numpyarray - np.mean(norm_numpyarray), sampled_signal)


    print("Highest peak is %2.3f: "%np.amax(correlated),end='')
    #peaks, _ = find_peaks(x, height=27)
    #peak_locations = np.take(a, argrelextrema(norm_correlated[a], np.greater)[0])

    #First, find the peaks. Points greater than their neighbors
    peak_locations = argrelextrema(correlated, np.greater)[0]
    #Filter the peaks >30. Noise generally around 24. True signal generally around 42.
    filtered_peak_locations = peak_locations[correlated[peak_locations] > 30]
    #Filter the peaks >0.8*Highest peak. Should allow for timing variations that cause poorer correlation.
    filtered_peak_locations = filtered_peak_locations[correlated[filtered_peak_locations] > 0.8*np.amax(correlated)]
    
    #Remove peaks that are too close together.
    #Subtract list from one offset by 1 to give distances between the peaks.
    distance_between_peaks = filtered_peak_locations[1:]-filtered_peak_locations[:-1]
    #Find where distance <60. Returns [False,False,True,..]
    to_remove = distance_between_peaks<60
    #Add a "Do not remove" to last peak. 
    #Needed since distance between peaks list is one shorter than filtered_peak_locations list.
    to_remove= np.append(to_remove,[False])
    #np.where(to_remove) #Which samples will be removed. Good for debug.
    #Delete peaks that are too close toegther.
    filtered_peak_locations = np.delete(filtered_peak_locations, np.where(to_remove))
    

    if plot:
        #Find y points for plotting
        y =  [norm_correlated[x] for x in filtered_peak_locations]
        plt.plot(filtered_peak_locations,y,'rs')

    print("Number of RN16 peaks is %i"%len(filtered_peak_locations),end='')
    return len(filtered_peak_locations)

def count(plot=False): #Use plot to allow calling from other (supervisor) functions
    # File operations
    f = scipy.fromfile(open(getcwd() + '/' + relative_path_to_file), dtype=scipy.float32)
    if Verbose:
        print("Number of datapoints is: %i"% f.size)

    #f = f[first_sample:last_sample]
    abs_f = abs(f[0::2] + 1j * f[1::2])
    try:
        abs_f = abs_f / np.amax(abs_f)
    except Exception as e:
        print("Error when normalising: \"%s\" "%e)
        return 0        
    # Matched filter to reduce hf noise
    abs_f = scipy.signal.correlate(abs_f, np.ones(decim), mode='same') / decim


    count_rn16 = count_rn16s_gate(abs_f,plot)

    if plot:
#        plt.plot(abs_f)
        plt.plot(np.around(abs_f/np.amax(abs_f)))   
        plt.show()
    return count_rn16

if __name__=='__main__':
    count(plot=True)
