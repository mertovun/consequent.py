import numpy as np
from scipy.signal import convolve

def apply_convolution_filter(amplitude, filter_kernel):
    filtered_amplitude = convolve(amplitude, filter_kernel, mode='same')
    return filtered_amplitude
