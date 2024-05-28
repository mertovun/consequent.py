import scipy.io.wavfile as wavfile
import numpy as np
from audio import load_audio_file, compute_spectrogram
from sine_fit.oscillator import save_oscillator_data, load_oscillator_data, extract_oscillator_data
from sine_fit.reconstruction import generate_output_signal, apply_lowpass_filter
from conv_mask.reconstruction import reconstruct_audio, apply_convolution_filters
from config import AUDIO_FILE, OUTPUT_AUDIO_FILE, SAMPLE_RATE, N_FFT, HOP_LENGTH

def main():
    y, sr = load_audio_file(AUDIO_FILE)
    amplitude, phase, frequencies = compute_spectrogram(y, sr)
    
    # Sine Oscillator Fit
    oscillator_data = extract_oscillator_data(amplitude, phase, frequencies)
    output_signal = generate_output_signal(oscillator_data, sr)
    output_signal = apply_lowpass_filter(output_signal, sr, 2000, 5)
    wavfile.write("sine_fit_" + OUTPUT_AUDIO_FILE, sr, output_signal.astype(np.float32))
    
    # Convolution Mask
    amplitude, phase, frequencies = compute_spectrogram(output_signal, sr)
    filtered_amplitude = apply_convolution_filters(amplitude)
    reconstructed_audio = reconstruct_audio(filtered_amplitude, phase, HOP_LENGTH, N_FFT)
    wavfile.write("conv_mask_" + OUTPUT_AUDIO_FILE, sr, reconstructed_audio.astype(np.float32))

    print(f"Generated audio saved to {OUTPUT_AUDIO_FILE}")

if __name__ == '__main__':
    main()
