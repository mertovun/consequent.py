import random
from scipy.signal import find_peaks
import json

from config import NUM_PEAKS, PeakSelection

def save_oscillator_data(oscillator_data, output_file):
    with open(output_file, 'w') as f:
        json.dump(oscillator_data, f, indent=4)

def load_oscillator_data(input_file):
    with open(input_file, 'r') as f:
        return json.load(f)

def extract_oscillator_data(amplitude, phase, frequencies):
    oscillator_data = []
    for time_slice_index in range(amplitude.shape[1]):
        amplitude_slice = amplitude[:, time_slice_index]
        phase_slice = phase[:, time_slice_index]

        peaks, _ = find_peaks(amplitude_slice, height=0.1)
        sorted_peaks = sorted(peaks, key=lambda peak: amplitude_slice[peak], reverse=True)[:NUM_PEAKS]

        peak_info = []
        for peak in sorted_peaks:
            A = amplitude_slice[peak].item()
            frequency_hz = frequencies[peak].item()
            phase_value = phase_slice[peak].item()

            peak_info.append({
                "frequency_hz": frequency_hz,
                "amplitude": A,
                "phase": phase_value
            })

        peak_info_sorted = sorted(peak_info, key=lambda x: x["frequency_hz"])
        oscillator_data.append({
            "time_slice_index": time_slice_index,
            "peaks": peak_info_sorted
        })

    return oscillator_data

def get_n_peaks(peaks, n, strategy=PeakSelection.HIGHEST):
    if strategy == PeakSelection.HIGHEST:
        sorted_peaks = sorted(peaks, key=lambda x: x['amplitude'], reverse=True)
    elif strategy == PeakSelection.LOWEST:
        sorted_peaks = sorted(peaks, key=lambda x: x['amplitude'])
    elif strategy == PeakSelection.RANDOM:
        sorted_peaks = random.sample(peaks, n) if len(peaks) > n else peaks
    return sorted_peaks[:n]