import scipy
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import numpy as np
from os import getcwd

# relative_path_to_file = '../data/Corilateme/source'
relative_path_to_file = '../misc/data/gate'
decim = 5  # decimation of matched filter
samp_rate = (2 * 10 ** 6) / decim  # Samples per second
half_symbol_length = int(round(12.5 * 10 ** -6 * samp_rate))
print("Sample rate is ", samp_rate)
print("Half symbol length is ", half_symbol_length)
# Reduce computation by specifying a range to look at
first_sample = 0
last_sample = 20000
verbose = False
plotit = True


def find_rn16(numpyarray):
    """Find the preamble of RN16 using cross-correlation"""
    # TODO downsample for speed, if reliable enough.
    sampled_signal = np.concatenate((2 * half_symbol_length * [1], half_symbol_length * [-1], half_symbol_length * [1],
                                     2 * half_symbol_length * [-1], half_symbol_length * [1],
                                     3 * half_symbol_length * [-1], half_symbol_length * [1]))
    # flipped = np.flipud(sampled_signal) #Usefull if convolving
    correlated = np.correlate(numpyarray - np.mean(numpyarray), sampled_signal)
    start_location = np.argmax(correlated)
    # plt.plot(correlated)
    # plt.show()
    # print("RN16 start loc is",start_location)
    return start_location

def end_rn16(numpyarray):
    """Find the end of RN16 using cross-correlation"""
    postamble =300
    # TODO downsample for speed, if reliable enough.
    sampled_signal = np.concatenate((half_symbol_length * [10],  postamble * [-1]))

    # flipped = np.flipud(sampled_signal) #Usefull if convolving
    correlated = np.correlate(numpyarray - np.mean(numpyarray), sampled_signal)
    end_rn16_loc = np.argmax(correlated)
    # plt.plot(correlated)
    # plt.show()
    # print("RN16 start loc is",start_location)
    return end_rn16_loc + half_symbol_length


def find_start_transmission(numpyarray):
    """Find the preamble of Transmission using cross-correlation"""
    prev_samples = 500
    start_transmit = np.concatenate((prev_samples * [1], half_symbol_length * [-100], half_symbol_length * [100],
                                     half_symbol_length * [-100], 2 * half_symbol_length * [100]))
    # Normalise, so midpoint is known.
    norm_numpyarray = numpyarray / np.amax(numpyarray)
    correlated = np.correlate(norm_numpyarray - 0.5, start_transmit)
    start_location = np.argmax(correlated) + prev_samples
    #plt.plot(correlated/350)
    #print("Transmission start loc is",start_location)
    return start_location


def find_end_transmission(numpyarray):
    """Find the last bit location of transmission using cross-correlation"""
    following_samples = 300
    start_transmit = np.concatenate((half_symbol_length * [-1], following_samples * [1]))
    norm_numpyarray = numpyarray / np.amax(numpyarray)
    correlated = np.correlate(norm_numpyarray - 0.5, start_transmit)
    start_location = np.argmax(correlated) + half_symbol_length
    # plt.plot(correlated)
    # plt.show()
    # print("Transmission end loc is",start_location)
    return start_location


# TODO remove when working state machine.
def find_initial_transmissions(numpyarray):
    # TODO allow this to change with frequency
    ds = 1
    downsampled = numpyarray[::ds]
    prev_samples = 700
    start_transmit = np.concatenate(
        (prev_samples / ds * [1], half_symbol_length / ds * [-1], half_symbol_length / ds * [1],
         half_symbol_length / ds * [-1], 2 * half_symbol_length / ds * [1]))

    # Assuming transmit>>received, normalising should make midpoint 0.5, thus 0.5 is not magic.
    norm_downsampled = downsampled / np.amax(downsampled)
    correlated = np.correlate(norm_downsampled - 0.5, start_transmit)
    # plt.plot(correlated)
    # plt.show()

    # TODO remove magic number
    # Need to find a way to find all of the high peaks for the given data.
    # Maybe generate the magic number dynamically eg correlated>max(correlated)-10
    # Since the transmissions will always be (roughly) the same amplitude after scaling, might not need to.
    a = np.where(correlated > 325)

    # print("Correlated is",correlated)
    start_locations = np.take(a, argrelextrema(correlated[a], np.greater)[
        0]) * ds + prev_samples  # Since started sampling 500 before the real signal
    # Finishes roughly 1800 later
    print("Transmission start loc is ", start_locations)
    return start_locations


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


    

def count_rn16s():
    """
    Count
    """
    global count_rn16
    relative_position = 0
    while(1):
        try:
            first_tran_start = find_start_transmission(
                abs_f[0 + relative_position:10000 + relative_position]) + relative_position
        except ValueError:
            return count_rn16
        # Searches for the end between 1500 and 2500 later than the start.
        min_trans, max_trans = 1200, 2500
        try:
            first_tran_end = find_end_transmission(
                abs_f[first_tran_start + min_trans:first_tran_start + max_trans]) + first_tran_start + min_trans
        except ValueError:
            return count_rn16
        if verbose:
            print("first_transm_loc", first_tran_start, first_tran_end)

        # Plot circles to show where signals have been detected.
        #if plotit:
        #    plt.plot([first_tran_start],1,'go')
        #    plt.plot([first_tran_end],1,'ro')


        # Read data between, see if we are RN16 or EPC
        start_rn16_loc = find_rn16(abs_f[first_tran_end + 100:first_tran_end + 1000]) + first_tran_end + 100
        if verbose:
            print("start rn16 loc is ", start_rn16_loc)


        #Assume looking at an RN16. If not, the data_len check will fail.
        end_rn16_loc = end_rn16(abs_f[start_rn16_loc - 50:start_rn16_loc + 1500])+start_rn16_loc - 50


        rn16_test = decode_rn16(abs_f[start_rn16_loc - 50:end_rn16_loc + 50], 7, 0)
        data_len = len(rn16_test)
        # if plotit:
        #     plt.plot([start_rn16_loc],1,'bo')
        #     plt.plot([end_rn16_loc],1,'co')

        if 17 > data_len > 14:
            # probably a RN16
            print("RN16 at location",start_rn16_loc)
            if verbose:
                print("Found a RN16", rn16_test, len(rn16_test))
            # Start position is the first transmsiion
            count_rn16+=1
            #if plotit:
           #     plt.plot([start_rn16_loc],1,'bo')
            #    plt.plot([end_rn16_loc],1,'co')
            relative_position = end_rn16_loc + 50

        else:
            # failed read
            if verbose:
                print(
                "Failed to read an EPC or RN16 in range ", start_rn16_loc - 50 + relative_position ,end_rn16_loc + 50 + relative_position, "datalen was",
                data_len, "LOOPING")
            relative_position = start_rn16_loc +1000

def count_rn16s_gate(numpyarray):
    """Find the preamble of RN16 using cross-correlation"""
    # TODO downsample for speed, if reliable enough.
    sampled_signal = np.concatenate((1 * half_symbol_length * [-1],
2 * half_symbol_length * [1], half_symbol_length * [-1], half_symbol_length * [1],
                                     2 * half_symbol_length * [-1], half_symbol_length * [1],
                                     3 * half_symbol_length * [-5], half_symbol_length * [1]))
    # flipped = np.flipud(sampled_signal) #Usefull if convolving
    correlated = np.correlate(numpyarray - np.mean(numpyarray), sampled_signal)
    norm_correlated =     correlated/ np.amax(correlated)
    if plotit:
        plt.plot(norm_correlated)
    
    #start_location = np.argmax(correlated)
    print("Highest peak is ",np.amax(correlated))
    a = np.where((correlated > 25) & (correlated>.9*np.amax(correlated)))#.9*np.amax(correlated))
    print(a)

    b = np.take(a, argrelextrema(norm_correlated[a], np.greater)[0])
    print(argrelextrema(norm_correlated[a], np.greater))
    y =  [norm_correlated[b_val]+0.2 for b_val in b]
    plt.plot(b,y,'rs')
    print("Number of RN16 peaks is ",len(b))
    return len(b)

def count():
    # File operations
    f = scipy.fromfile(open(getcwd() + '/' + relative_path_to_file), dtype=scipy.float32)
    if verbose:
        print("Number of datapoints is:", f.size)
    #f = f[first_sample:last_sample]
    abs_f = abs(f[0::2] + 1j * f[1::2])
    abs_f = abs_f / np.amax(abs_f)
    # Matched filter to reduce hf noise
    abs_f = scipy.signal.correlate(abs_f, np.ones(decim), mode='same') / decim


    count_rn16 = count_rn16s_gate(abs_f)

    if __name__=='__main__':
        plt.plot(abs_f)
        plt.show()
    return count_rn16

if __name__=='__main__':
    count()
