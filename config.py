
BPM = 120

# Audio File Parameters
AUDIO_FILE = 'input_audio.wav'  # Input audio file path
OUTPUT_FILE = 'oscillator_values.json'  # Output oscillator values file path
OUTPUT_AUDIO_FILE = 'output_audio'  # Input audio file path

from enum import Enum

class PeakSelection(Enum):
    HIGHEST = 'highest'
    LOWEST = 'lowest'
    RANDOM = 'random'

SERIES = True

SINE_FIT_CONFIGS = [
        {
        'N_FFT': 2048,
        'HOP_LENGTH': 4096,
        'NUM_PEAKS': 4,
        'PEAK_SELECTION_STRATEGY': PeakSelection.HIGHEST,
        'N_PEAKS': 4,
        'APPLY_HANNING': True,
        'HANNING_DEGREE': 0.6,
        'INCLUDE_PHASE': True,
        'PHASE_DEGREE': 1.0,
        'APPLY_SCALE': False,
        'BASE_NOTE': 'E',
        'SCALING_COEFFICIENTS': [.99, .0, .6, .7, .0, .5, .1, .8, .6, .0, .4, .0],
        'APPLY_GLIDING': False,
        'GLIDE_THRESHOLD_MAX': 12.0,
        'GLIDE_THRESHOLD_MIN': 5.0,
        'CUTOFF_FREQUENCY': 2000,
        'FILTER_ORDER': 5,
        'SR_COEFFICIENT': 1,
    },
    {
        'N_FFT': 2048,
        'HOP_LENGTH': 4096,
        'NUM_PEAKS': 16,
        'PEAK_SELECTION_STRATEGY': PeakSelection.HIGHEST,
        'N_PEAKS': 16,
        'APPLY_HANNING': True,
        'HANNING_DEGREE': 0.6,
        'INCLUDE_PHASE': True,
        'PHASE_DEGREE': 1.0,
        'APPLY_SCALE': False,
        'BASE_NOTE': 'E',
        'SCALING_COEFFICIENTS': [.99, .0, .6, .7, .0, .5, .1, .8, .6, .0, .4, .0],
        'APPLY_GLIDING': False,
        'GLIDE_THRESHOLD_MAX': 12.0,
        'GLIDE_THRESHOLD_MIN': 5.0,
        'CUTOFF_FREQUENCY': 3000,
        'FILTER_ORDER': 5,
        'SR_COEFFICIENT': 2,
    },
]
