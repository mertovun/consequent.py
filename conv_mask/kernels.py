import numpy as np
from scipy.signal import convolve

def apply_convolution_filter(amplitude, filter_kernel):
    return convolve(amplitude, filter_kernel, mode='same')

def apply_kernels_in_series(amplitude, kernels):
    filtered_amplitude = amplitude
    for kernel in kernels:
        filtered_amplitude = apply_convolution_filter(filtered_amplitude, kernel)
    return filtered_amplitude

def apply_kernels_in_parallel(amplitude, kernels):
    filtered_amplitudes = [apply_convolution_filter(amplitude, kernel) for kernel in kernels]
    return np.mean(filtered_amplitudes, axis=0)

def get_kernel(kernel_name):
    kernels = {
        'average': np.ones((5, 5)) / 25,
        'gaussian': np.array([[1, 4, 7, 4, 1],
                              [4, 16, 26, 16, 4],
                              [7, 26, 41, 26, 7],
                              [4, 16, 26, 16, 4],
                              [1, 4, 7, 4, 1]]) / 273,
        'sharpen': np.array([[0, -1, 0],
                             [-1, 5, -1],
                             [0, -1, 0]]),
        'laplacian': np.array([[0, 1, 0],
                             [1, -4, 1],
                             [0, 1, 0]]),
        'sobel_time': np.array([[-1, 0, 1],
                                [-2, 0, 2],
                                [-1, 0, 1]]),
        'sobel_time_reverse': np.array([[1, 0, -1],
                                [2, 0, -2],
                                [1, 0, -1]]),                                
        'sobel_freq': np.array([[-1, -2, -1],
                                [0, 0, 0],
                                [1, 2, 1]]),
        'identity': np.array([[0, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 0]])
    }
    return kernels.get(kernel_name, np.ones((3, 3)) / 9)  # Default to a simple average kernel if not found
