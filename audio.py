import numpy as np
import librosa

from config import HOP_LENGTH, N_FFT

def load_audio_file(audio_file):
    y, sr = librosa.load(audio_file)
    return y, sr

def compute_spectrogram(y, sr, n_fft=N_FFT, hop_length=HOP_LENGTH):
    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    amplitude = np.abs(S)
    phase = np.angle(S)
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=N_FFT)
    return amplitude, phase, frequencies