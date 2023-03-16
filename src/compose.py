import musical_params
import synth
import numpy as np
import os
import gensound
from gensound.signals import Sine, Sawtooth, Square, Triangle, WhiteNoise, Silence, PinkNoise, Mix, WAV
from gensound.effects import OneImpulseReverb, Vibrato
from gensound.filters import SimpleBandPass, SimpleHPF, SimpleLPF, SimpleHighShelf, SimpleLowShelf
from gensound.transforms import ADSR, Fade, Amplitude, CrossFade,Shift

def check_range(num):
    if num < 24:
        return check_range(num+12)
    elif num > 60:
        return check_range(num-12)
    else:
        return num


dur = 3*60

starting_key = np.random.choice(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'])
starting_note_density = np.random.choice([1,2,3,4,5])
starting_length = np.random.choice(["VS", "S", "M", "L", "VL"])

params={"default":{
            "composition_probabilities":[0.5,0.5], 
            "key_transition_probability":[0.3,0.3,0.3,0.1], 
            "key_type":"major", 
            "note_density_transition_matrix":[[0.0,0.0,0.4,0.35,0.25],
                                             [0.00,0.1,0.4,0.3,0.2],
                                             [0.0,0.05,0.5,0.25,0.2],
                                             [0.05,0.0,0.45,0.25,0.25],
                                             [0.05,0.05,0.4,0.3,0.2]],
            "octave_transition_matrix":[[0.1,0.8,0.05,0.05], 
            [0.1,0.7,0.15,0.05], 
            [0.05,0.6,0.35,0.0], 
            [0.1,0.4,0.4,0.1]],
            "duration_transition_matrix":[[0.1,0.1,0.5,0.15,0.15],
                                         [0.1,0.1,0.5,0.15,0.15],
                                         [0.1,0.1,0.5,0.15,0.15],
                                         [0.1,0.1,0.5,0.15,0.15],
                                         [0.1,0.1,0.5,0.15,0.15]]
        },
    "1":{
            "composition_probabilities":[0.5,0.5], 
            "key_transition_probability":[0.3,0.3,0.3,0.1], 
            "key_type":"major", 
            "note_density_transition_matrix":[[0.0,0.0,0.4,0.35,0.25],
                                             [0.00,0.1,0.4,0.3,0.2],
                                             [0.0,0.05,0.5,0.25,0.2],
                                             [0.05,0.0,0.45,0.25,0.25],
                                             [0.05,0.05,0.4,0.3,0.2]],
            "octave_transition_matrix":[[0.1,0.8,0.05,0.05], 
            [0.1,0.7,0.15,0.05], 
            [0.05,0.6,0.35,0.0], 
            [0.1,0.4,0.4,0.1]],
            "duration_transition_matrix":[[0.1,0.1,0.5,0.15,0.15],
                                         [0.1,0.1,0.5,0.15,0.15],
                                         [0.1,0.1,0.5,0.15,0.15],
                                         [0.1,0.1,0.5,0.15,0.15],
                                         [0.1,0.1,0.5,0.15,0.15]]
        }
}
mp = musical_params.MusicalParameters(
                                duration=dur, 
                                ending_chord_min_length=2, 
                                starting_key=starting_key, 
                                starting_length=starting_length, 
                                starting_note_density=starting_note_density, 
                                starting_octave=4, 
                                preset_dict = params)

arr=mp.get_musical_parameters({0.0:1,dur:1})
print(arr)
synth_params = {
        'lfo1_type': 'sine',
        'lfo1_freq': 0.5, # for focus
        'lfo1_depth': 0.5,

        'lfo2_type': 'sine',
        'lfo2_freq': 0.5, # slow wobble
        'lfo2_depth': 0.25,
        
        'osc1_wave': 'triangle',
        'osc1_detune': 5,

        'osc2_wave': 'square',
        'osc2_detune': 5,
        'osc2_relative_shift': 8,

        'n_voices': 8, # too high and this introduces a phaser efect

        'sub_freq': 30,
        'sub_wave': 'sine',
        'sub_detune': 0,

        'hf_noise_type': 'pink', # na/white/pink

        'lf_noise_type': 'na',

        'filter1_type': 'lowpass',
        'filter1_freq': 200,

        'filter2_type': 'na',
        'filter2_freq': 0,

        'filter3_type': 'na',
        'filter3_freq': 0,

        'reverb': 0.5,

        'vibrato_freq': 0,
        'vibrato_depth': 0,

        'attack': 780.0,
        'decay': 0.05,
        'sustain': 0.9,
        'release': 408.0,

        'fade_in': 0.5,
        'fade_out': 0.5,
        }
s = synth.Synth(synth_params)
chords = arr['chords']
durs = arr['durations']
# for note in chord:
audio=gensound.Signal()
for i in range(len(chords)):
    chord = chords[i]
    out_tx = Shift(-0.25e3)#Fade(is_in=True,duration=0.25e3)*Shift(-0.25e3)
    # in_tx = 
    b = np.random.choice([True, False], p=[0.2, 0.8])
    d=durs[i]*1e3
    if i == 0:
        if b:
            audio = audio | (gensound.mix([s.generate_audio(check_range(note), d) for note in chord]))
        else:
            arr1=[s.generate_audio(check_range(note)-24, (durs[i]*1e3)) for note in chord]
            arr2=[s.generate_audio(check_range(note)-12, (durs[i]*1e3)) for note in chord]
            arr3=[s.generate_audio(check_range(note), (durs[i]*1e3)) for note in chord]
            
            audio = audio | (gensound.mix(arr1+arr2+arr3))#*out_tx
    else:
        if b:
            audio = audio*Fade(is_in=False,duration=durs[i-1]*0.2*1e3) | (gensound.mix([s.generate_audio(check_range(note)-24, (durs[i]*1e3)) for note in chord]))*Fade(is_in=True, duration=0.3*durs[i]*1e3)#*out_tx
        else:
            arr1=[s.generate_audio(check_range(note)-24, (durs[i]*1e3)) for note in chord]
            arr2=[s.generate_audio(check_range(note)-12, (durs[i]*1e3)) for note in chord]
            arr3=[s.generate_audio(check_range(note), (durs[i]*1e3)) for note in chord]
            
            audio = audio*Fade(is_in=False,duration=durs[i-1]*0.2*1e3) | (gensound.mix(arr1+arr2+arr3))*Fade(is_in=True, duration=0.3*durs[i]*1e3)#*out_tx
        audio = audio 
# audio.play()
audio.export('composition.wav')