from enum import Enum
class PeakSelection(Enum):
    HIGHEST = 'highest'
    LOWEST = 'lowest'
    RANDOM = 'random'

# Spectrogram Parameters
N_FFT = 2048
HOP_LENGTH = 2048

# Peak Finding Parameters
NUM_PEAKS = 16  # Number of peaks to fit

# Reconstruction Parameters
PEAK_SELECTION_STRATEGY = PeakSelection.LOWEST 
PEAK_OFFSET = 2
N_PEAKS = 16                     # Number of peaks to select
USE_HIGHEST_AMPLITUDE = False   # Use highest amplitude peaks if True, otherwise use lowest

APPLY_HANNING = True            # Apply Hanning window
HANNING_DEGREE = 0.2            # Degree of Hanning window application
INCLUDE_PHASE = True           # Include phase in sine wave generation
PHASE_DEGREE = 1.0              # Degree to include phase

# Base Note and Note Scaling Coefficients
APPLY_SCALE = False
BASE_NOTE = 'E'
SCALING_COEFFICIENTS = [
    .99,    # 0    
    .0,     # 1
    .0,     # 2
    .0,     # 3
    .0,     # 4
    .0,     # 5
    .0,     # 6
    .8,     # 7
    .0,     # 8
    .0,     # 9
    .0,     # 10
    .0      # 11
]

# Gliding Effect Parameters
APPLY_GLIDING = True            # Enable gliding effect between timeslices
GLIDING_THRESHOLD_HALFTONES = 2.0  # Halftone threshold for gliding effect among neighboring peaks

# Low-Pass Filter Parameters
CUTOFF_FREQUENCY = 2000         # Cutoff frequency for Butterworth LPF
FILTER_ORDER = 5                # Order of the Butterworth LPF

# Audio File Parameters
AUDIO_FILE = 'input_audio.wav'  # Input audio file path
OUTPUT_FILE = 'oscillator_values.json'  # Output oscillator values file path
OUTPUT_AUDIO_FILE = 'output.wav'  # Input audio file path
SAMPLE_RATE = 44100  # Sample rate for output audio file
