from enum import Enum

class PeakSelection(Enum):
    HIGHEST = 'highest'
    LOWEST = 'lowest'
    RANDOM = 'random'

# Peak Finding Parameters
NUM_PEAKS = 16  # Number of peaks to fit

# Reconstruction Parameters
PEAK_SELECTION_STRATEGY = PeakSelection.HIGHEST 
# TODO: PEAK_OFFSET = 2
N_PEAKS = 16                     # Number of peaks to select from fits

APPLY_HANNING = True            # Apply Hanning window
HANNING_DEGREE = 0.3            # Degree of Hanning window application
INCLUDE_PHASE = False           # Include phase in sine wave generation
PHASE_DEGREE = 1.0              # Degree to include phase

# Base Note and Note Scaling Coefficients
APPLY_SCALE = False
BASE_NOTE = 'E'
SCALING_COEFFICIENTS = [
    .99,    # 0    
    .0,     # 1
    .0,     # 2
    .8,     # 3
    .0,     # 4
    .7,     # 5
    .0,     # 6
    .9,     # 7
    .0,     # 8
    .0,     # 9
    .6,     # 10
    .0      # 11
]

# Gliding Effect Parameters
APPLY_GLIDING = True            # Enable gliding effect between timeslices
GLIDE_THRESHOLD_MAX = 36.0  # Halftone threshold for gliding effect among neighboring peaks
GLIDE_THRESHOLD_MIN = 0.0  # Halftone threshold for gliding effect among neighboring peaks

# Low-Pass Filter Parameters
CUTOFF_FREQUENCY = 2000         # Cutoff frequency for Butterworth LPF
FILTER_ORDER = 5                # Order of the Butterworth LPF

