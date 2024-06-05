import numpy as np
import librosa

def load_audio_file(audio_file):
    y, sr = librosa.load(audio_file)
    return y, sr

def compute_spectrogram(y, sr, config):
    S = librosa.stft(y, n_fft=config['N_FFT'], hop_length=config["HOP_LENGTH"])
    amplitude = np.abs(S)
    phase = np.angle(S)
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=config['N_FFT'])
    return amplitude, phase, frequencies