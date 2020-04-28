import scipy
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import numpy as np
from os import getcwd
from array import array

relative_path_to_file = '../misc/data/master'
decim = 5  # decimation of matched filter


f = scipy.fromfile(open(getcwd() + '/' + relative_path_to_file), dtype=scipy.float32)
#abs_f = abs(f[0::2] + 1j * f[1::2])
#plt.plot(abs_f[77000:87000])
#plt.plot(abs_f)
# Adding noise using target SNR

# Set a target SNR
target_snr_db = 8
# Calculate signal power and convert to dB 
sig_avg_watts = 0.26*0.25
sig_avg_db = 10 * np.log10(sig_avg_watts)
# Calculate noise according to [2] then convert to watts
noise_avg_db = sig_avg_db - target_snr_db
noise_avg_watts = 10 ** (noise_avg_db / 10)
# Generate an sample of white noise
mean_noise = 0
noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(f))
# Noise up the original signal

f = f + noise_volts
f = f.astype(scipy.float32)
abs_f = abs(f[0::2] + 1j * f[1::2])
#plt.plot(abs_f)#[77000:87000])
plt.show()

output_file = open(getcwd() + '/'+'../misc/data/out', 'wb')
f.tofile(output_file)
output_file.close()
