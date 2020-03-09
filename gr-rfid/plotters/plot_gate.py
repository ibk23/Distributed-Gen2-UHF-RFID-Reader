import scipy
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import numpy as np
from os import getcwd

relative_path_to_file = '../misc/data/gate'
decim = 5  # decimation of matched filter


f = scipy.fromfile(open(getcwd() + '/' + relative_path_to_file), dtype=scipy.float32)

abs_f = abs(f[0::2] + 1j * f[1::2])
abs_f = abs_f[1::5]
abs_f = abs_f / np.amax(abs_f)
#abs_f = abs_f[145:-1]
# Matched filter to reduce hf noise
#abs_f = scipy.signal.correlate(abs_f, np.ones(decim), mode='same') / decim


plt.plot(abs_f)   
plt.show();
