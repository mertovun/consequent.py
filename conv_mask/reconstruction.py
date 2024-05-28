import numpy as np
import librosa
from conv_mask.kernels import apply_kernels_in_series, apply_kernels_in_parallel, get_kernel
from conv_mask.config import KERNELS_TO_APPLY, KERNEL_APPLICATION_MODE, KernelApplicationMode

def reconstruct_audio(filtered_amplitude, phase, hop_length, n_fft):
    S_filtered = filtered_amplitude * np.exp(1j * phase)
    y_reconstructed = librosa.istft(S_filtered, hop_length=hop_length, n_fft=n_fft)
    return y_reconstructed

def apply_convolution_filters(amplitude):
    kernels = [get_kernel(kernel_name) for kernel_name in KERNELS_TO_APPLY]
    if KERNEL_APPLICATION_MODE == KernelApplicationMode.SERIES:
        return apply_kernels_in_series(amplitude, kernels)
    elif KERNEL_APPLICATION_MODE == KernelApplicationMode.PARALLEL:
        return apply_kernels_in_parallel(amplitude, kernels)
    return amplitude