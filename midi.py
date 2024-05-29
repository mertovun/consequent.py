# midi_output.py
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
import numpy as np

from config import BPM, HOP_LENGTH

def frequency_to_midi_note_number(frequency):
    if frequency <= 0:
        return None
    note = int(69 + 12 * np.log2(frequency / 440.0))
    note = max(0, min(127, note))
    return note

def create_midi_file(oscillator_data, output_file, sample_rate):
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(BPM)))
    
    time_slice_duration = HOP_LENGTH / sample_rate
    ticks_per_beat = midi.ticks_per_beat  # Get ticks per beat from the MIDI file
    ms_per_beat = bpm2tempo(BPM) / 1000  # Convert microseconds to milliseconds (assuming 120 BPM)
    ticks_per_ms = ticks_per_beat / ms_per_beat  # Calculate ticks per millisecond

    
    for time_slice_index, time_slice in enumerate(oscillator_data[:-1]):
        next_time_slice = oscillator_data[time_slice_index + 1]
        peaks = time_slice['peaks']
        next_peaks = next_time_slice['peaks']
        
        t = np.linspace(time_slice_index * time_slice_duration, (time_slice_index + 1) * time_slice_duration, int(sample_rate * time_slice_duration), endpoint=False)
        
        for peak, next_peak in zip(peaks, next_peaks):
            start_freq = peak['frequency_hz']
            end_freq = next_peak['frequency_hz']
            start_amp = peak['amplitude']
            end_amp = next_peak['amplitude']
            # start_phase = peak['phase']
            # end_phase = next_peak['phase']
            
            for time_step in t:
                frequency = start_freq + (end_freq - start_freq) * time_step / time_slice_duration
                if frequency <= 0:
                    continue
                
                pitch_bend_amount = int(((end_freq - start_freq) * time_step / time_slice_duration) * 8192 / 12)
                pitch_bend_amount = max(-8192, min(8191, pitch_bend_amount))  # Ensure pitch bend amount is within the valid range
                
                note = frequency_to_midi_note_number(frequency)
                if note is None:
                    continue
                
                velocity = int((start_amp + (end_amp - start_amp) * time_step / time_slice_duration) * 127)
                velocity = max(0, min(127, velocity))  # Ensure velocity is within the valid range
                
                time_ticks = int(time_step * 1000 * ticks_per_ms)  # Convert time_step to ticks
                
                track.append(Message('pitchwheel', pitch=pitch_bend_amount, time=time_ticks))
                track.append(Message('note_on', note=note, velocity=velocity, time=time_ticks))
                track.append(Message('note_off', note=note, velocity=0, time=time_ticks))
    
    midi.save(output_file)



def add_mpe_gliding(track, oscillator_data, sample_rate):
    time_slice_duration = 1 / sample_rate
    for i, time_slice in enumerate(oscillator_data[:-1]):
        next_time_slice = oscillator_data[i + 1]
        current_peaks = time_slice['peaks']
        next_peaks = next_time_slice['peaks']
        
        for current_peak, next_peak in zip(current_peaks, next_peaks):
            current_note = frequency_to_midi_note_number(current_peak['frequency_hz'])
            next_note = frequency_to_midi_note_number(next_peak['frequency_hz'])
            
            if current_note != next_note:
                time = int(time_slice_duration * 1000)
                pitch_bend_amount = (next_note - current_note) * 8192 // 12  # Assuming 12 semitones range for pitch bend
                
                track.append(Message('pitchwheel', pitch=pitch_bend_amount, time=time))

