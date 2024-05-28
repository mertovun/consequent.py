import random
import numpy as np
from scipy.signal import butter, lfilter
from config import (
    APPLY_GLIDING, APPLY_HANNING, GLIDING_THRESHOLD_HALFTONES, HANNING_DEGREE, N_PEAKS, PEAK_SELECTION_STRATEGY,
    INCLUDE_PHASE, PHASE_DEGREE, APPLY_SCALE, BASE_NOTE, SCALING_COEFFICIENTS
)
from notes import frequency_to_halftones, map_frequency_to_note_and_scale
from oscillator import get_n_peaks

def apply_partial_hanning(signal_slice, degree):
    hanning_window = np.hanning(len(signal_slice))
    return signal_slice * (1 - degree) + signal_slice * hanning_window * degree

def glide_between_peaks(start_freq, end_freq, start_amp, end_amp, start_phase, end_phase, t, duration):
    t_normalized = t / duration
    frequencies = start_freq + (end_freq - start_freq) * t_normalized
    amplitudes = start_amp + (end_amp - start_amp) * t_normalized
    phases = start_phase + (end_phase - start_phase) * t_normalized
    return amplitudes * np.sin(2 * np.pi * frequencies * t + phases)

def generate_output_signal(oscillator_data, sample_rate, time_slice_duration):
    output_signal = []
    num_slices = len(oscillator_data)
    for time_slice in oscillator_data:
        time_slice_index = time_slice['time_slice_index']
        peaks = time_slice['peaks']
        
        top_peaks = get_n_peaks(peaks, N_PEAKS, strategy=PEAK_SELECTION_STRATEGY)
        
        t = np.linspace(time_slice_index * time_slice_duration, (time_slice_index + 1) * time_slice_duration, int(sample_rate * time_slice_duration), endpoint=False)
        
        signal_slice = np.zeros_like(t)
        
        for i, peak in top_peaks:
            frequency = peak['frequency_hz']
            amplitude = peak['amplitude']
            phase = peak['phase'] if INCLUDE_PHASE else 0
            
            if APPLY_SCALE:
                scale = map_frequency_to_note_and_scale(frequency, BASE_NOTE, SCALING_COEFFICIENTS)
                amplitude *= scale 

            if not np.isnan(phase):
                if APPLY_GLIDING and time_slice_index < num_slices - 1:
                    next_peaks = get_n_peaks(oscillator_data[time_slice_index + 1]['peaks'], N_PEAKS, strategy=PEAK_SELECTION_STRATEGY)
                    next_peak = next((p for p in next_peaks if abs(frequency_to_halftones(frequency, p['frequency_hz'])) < GLIDING_THRESHOLD_HALFTONES), None)
                    if next_peak:
                        signal_slice += glide_between_peaks(
                            frequency, next_peak['frequency_hz'], 
                            amplitude, next_peak['amplitude'], 
                            phase, next_peak['phase'] if INCLUDE_PHASE else 0, 
                            t, time_slice_duration
                        )
                    else:
                        signal_slice += amplitude * np.sin(2 * np.pi * frequency * t + phase * PHASE_DEGREE)
                else:
                    signal_slice += amplitude * np.sin(2 * np.pi * frequency * t + phase * PHASE_DEGREE)


        
        if APPLY_HANNING:
            signal_slice = apply_partial_hanning(signal_slice, HANNING_DEGREE)

        output_signal.extend(signal_slice)
    
    output_signal = np.array(output_signal)
    output_signal = output_signal / np.max(np.abs(output_signal))
    return output_signal

def apply_lowpass_filter(output_signal, sample_rate, cutoff_frequency, filter_order=5):
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff_frequency / nyquist
    b, a = butter(filter_order, normal_cutoff, btype='low', analog=False)
    filtered_signal = lfilter(b, a, output_signal)
    normalized_signal = filtered_signal / np.max(np.abs(filtered_signal))
    return normalized_signal
