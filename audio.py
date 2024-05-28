import numpy as np
import librosa

from config import N_FFT, HOP_LENGTH, NUM_PEAKS

def load_audio_file(audio_file):
    y, sr = librosa.load(audio_file)
    S = librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH)
    amplitude = np.abs(S)
    phase = np.angle(S)
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=N_FFT)
    return amplitude, phase, frequencies, sr
