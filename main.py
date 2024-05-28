# main.py

import scipy.io.wavfile as wavfile
import numpy as np
from config import HOP_LENGTH, OUTPUT_AUDIO_FILE, SAMPLE_RATE, AUDIO_FILE, OUTPUT_FILE, CUTOFF_FREQUENCY, FILTER_ORDER
from audio import load_audio_file
from oscillator import save_oscillator_data, load_oscillator_data, extract_oscillator_data
from signal_reconstruction import generate_output_signal, apply_lowpass_filter

def main():

    amplitude, phase, frequencies, sr = load_audio_file(AUDIO_FILE)
    
    oscillator_data = extract_oscillator_data(amplitude, phase, frequencies)

    # save_oscillator_data(oscillator_data, OUTPUT_FILE)
    # oscillator_data = load_oscillator_data(OUTPUT_FILE)
    
    time_slice_duration = 2 * HOP_LENGTH / SAMPLE_RATE
    output_signal = generate_output_signal(oscillator_data, SAMPLE_RATE, time_slice_duration)
    output_signal = apply_lowpass_filter(output_signal, SAMPLE_RATE, CUTOFF_FREQUENCY, FILTER_ORDER)
    
    # Step 8: Save the filtered signal to a WAV file
    wavfile.write(OUTPUT_AUDIO_FILE, SAMPLE_RATE, output_signal.astype(np.float32))
    print(f"Generated audio saved to {OUTPUT_AUDIO_FILE}")

if __name__ == '__main__':
    main()
