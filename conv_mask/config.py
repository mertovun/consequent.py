from enum import Enum

class KernelApplicationMode(Enum):
    SERIES = 'series'
    PARALLEL = 'parallel'

# Convolution Filter Parameters
KERNELS_TO_APPLY = ['sobel_time']  # List of kernel names to apply
KERNEL_APPLICATION_MODE = KernelApplicationMode.SERIES  # Apply kernels in series or parallel
