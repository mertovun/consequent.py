import scipy.io.wavfile as wavfile
import numpy as np
from audio import load_audio_file, compute_spectrogram
from sine_fit.oscillator import extract_oscillator_data
from sine_fit.reconstruction import generate_output_signal, apply_lowpass_filter
from config import AUDIO_FILE, OUTPUT_AUDIO_FILE, SERIES, SINE_FIT_CONFIGS

def mix_signals(signals):
    max_length = max(len(signal) for signal in signals)
    mixed_signal = np.zeros(max_length)
    for signal in signals:
        mixed_signal[:len(signal)] += signal
    mixed_signal /= len(signals)
    return mixed_signal

def main():
    y, sr = load_audio_file(AUDIO_FILE)

    all_output_signals = []

    for idx, config in enumerate(SINE_FIT_CONFIGS):
        amplitude, phase, frequencies = compute_spectrogram(y, sr, config)
        oscillator_data = extract_oscillator_data(amplitude, phase, frequencies, config)
        output_signal = generate_output_signal(oscillator_data, sr*config['SR_COEFFICIENT'], config)
        output_signal = apply_lowpass_filter(output_signal, sr*config['SR_COEFFICIENT'], config['CUTOFF_FREQUENCY'], config['FILTER_ORDER'])
        if SERIES:
            y = output_signal
        all_output_signals.append(output_signal)
        output_filename = f'{OUTPUT_AUDIO_FILE}_{idx}.wav'
        wavfile.write(output_filename, sr, output_signal.astype(np.float32))
        print(f"Generated audio saved to {output_filename}")

if __name__ == '__main__':
    main()
