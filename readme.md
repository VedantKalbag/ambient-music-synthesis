# Emotion Conditioned Ambient Music Synthesis
![Tests](https://github.com/VedantKalbag/emotional-background-music-generation/actions/workflows/tests.yaml/badge.svg)

This library is built to synthesize ambient music based on emotion cues. These cues are passed to the system in the form of valence-arousal segments created from Russell's circumplex model.

The 5 segments shown below represent the 4 quadrants along with a "neutral" segment (#5).
The input to the system is a dictionary mapping of the various segments desired and the timestamps at which they are to be present (eg. ``` {time1:segment1, time2:segment2, etc.} ```), and the system will synthesize an audio file matching this mapping, with smooth transitions from one segment to another.

<img src="https://user-images.githubusercontent.com/42708932/206747869-66d2026e-e71d-4912-bfba-6c9f64ec5a14.png" width="300" height="300" />



Future work:
The synthesis will have different themes for generation, which will control the overall type of the output. Examples include:  
- minimal
- drone
- lush
- busy
- voice/choir style sounds
