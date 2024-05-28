import numpy as np

NOTE_FREQUENCIES = {
    'A': 440.0,
    'A#': 466.16,
    'B': 493.88,
    'C': 523.25,
    'C#': 554.37,
    'D': 587.33,
    'D#': 622.25,
    'E': 659.25,
    'F': 698.46,
    'F#': 739.99,
    'G': 783.99,
    'G#': 830.61
}

def map_frequency_to_note_and_scale(frequency, base_note, scaling_coefficients):
    min_diff = float('inf')
    note_index = 0
    while (frequency < 437.5):
        frequency *= 2
    while (frequency >= 875.0):
        frequency /= 2
    for idx, (_, note_freq) in enumerate(NOTE_FREQUENCIES.items()):
        diff = abs(frequency - note_freq)
        if diff < min_diff:
            min_diff = diff
            note_index = idx

    base_note_index = list(NOTE_FREQUENCIES.keys()).index(base_note)
    relative_index = (note_index - base_note_index) % 12

    return scaling_coefficients[relative_index]

def frequency_to_halftones(f1, f2):
    return 12 * np.log2(f2 / f1)