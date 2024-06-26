import numpy as np
from scipy.signal import butter, lfilter
from notes import frequency_to_halftones, map_frequency_to_note_and_scale
from sine_fit.oscillator import get_n_peaks

def apply_partial_hanning(signal_slice, degree):
    hanning_window = np.hanning(len(signal_slice))
    return signal_slice * (1 - degree) + signal_slice * hanning_window * degree

def glide_between_peaks(start_freq, end_freq, start_amp, end_amp, start_phase, end_phase, t, duration):
    t_normalized = t / duration
    frequencies = start_freq + (end_freq - start_freq) * t_normalized
    amplitudes = start_amp + (end_amp - start_amp) * t_normalized
    phases = start_phase + (end_phase - start_phase) * t_normalized
    return amplitudes * np.sin(2 * np.pi * frequencies * t + phases)

def generate_output_signal(oscillator_data, sample_rate, config):
    time_slice_duration = config['HOP_LENGTH'] / sample_rate
    output_signal = []
    num_slices = len(oscillator_data)
    for time_slice in oscillator_data:
        time_slice_index = time_slice['time_slice_index']
        peaks = time_slice['peaks']
        
        top_peaks = get_n_peaks(peaks, config['N_PEAKS'], strategy=config['PEAK_SELECTION_STRATEGY'])
        
        t = np.linspace(time_slice_index * time_slice_duration, (time_slice_index + 1) * time_slice_duration, int(sample_rate * time_slice_duration), endpoint=False)
        
        signal_slice = np.zeros_like(t)
        
        for peak in top_peaks:
            frequency = peak['frequency_hz']
            amplitude = peak['amplitude']
            phase = peak['phase'] if config['INCLUDE_PHASE'] else 0
            
            if config['APPLY_SCALE']:
                scale = map_frequency_to_note_and_scale(frequency, config['BASE_NOTE'], config['SCALING_COEFFICIENTS'])
                amplitude *= scale 

            if not np.isnan(phase):
                if config['APPLY_GLIDING'] and time_slice_index < num_slices - 1:
                    next_peaks = get_n_peaks(oscillator_data[time_slice_index + 1]['peaks'], config['N_PEAKS'], strategy=config['PEAK_SELECTION_STRATEGY'])
                    next_peak = min(next_peaks, key=lambda p: abs(frequency_to_halftones(frequency, p['frequency_hz'])), default=None)
                    if next_peak:
                        glide_freq_diff = abs(frequency_to_halftones(frequency, next_peak['frequency_hz']))
                        if glide_freq_diff <= config['GLIDE_THRESHOLD_MAX'] and glide_freq_diff >= config['GLIDE_THRESHOLD_MIN']:
                            signal_slice += glide_between_peaks(
                                frequency, next_peak['frequency_hz'], 
                                amplitude, next_peak['amplitude'], 
                                phase, next_peak['phase'] if config['INCLUDE_PHASE'] else 0, 
                                t, time_slice_duration
                            )
                        else:
                            signal_slice += amplitude * np.sin(2 * np.pi * frequency * t + phase * config['PHASE_DEGREE'])
                    else:
                        signal_slice += amplitude * np.sin(2 * np.pi * frequency * t + phase * config['PHASE_DEGREE'])
                else:
                    signal_slice += amplitude * np.sin(2 * np.pi * frequency * t + phase * config['PHASE_DEGREE'])
        
        if config['APPLY_HANNING']:
            signal_slice = apply_partial_hanning(signal_slice, config['HANNING_DEGREE'])

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
