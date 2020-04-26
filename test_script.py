from scipy.io import wavfile
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
import numpy as np
import ecoacoustics

# Load a sound from a wav file
filename = './audio/LINE_2003-10-30_20_00_34.wav'

## Calculate acoustic indices

# All indices of interest can be ported from https://github.com/ljvillanueva/soundecology
# They go for 512-point hamming

# Acoustic Complexity Index (ACI)
# - A new methodology to infer the singing activity of an avian community: The Acoustic Complexity Index (ACI)
aic = ecoacoustics.acoustic_complexity(filename)

# Acoustic Diversity Index (ADI)
adi = ecoacoustics.acoustic_diversity(data, fs)

# Acoustic Evenness (AEve)
aeve = ecoacoustics.acoustic_evenness(data, fs)

# Bioacoustic Index (Bio)
bio = ecoacoustics.bioacoustic_index(data, fs)

# Acoustic Entropy (H)
h = ecoacoustics.acoustic_entropy(data, fs)

# Median of the amplitude envelope (M)
medenv = ecoacoustics.median_envelope(data, fs)

# Normalized Difference Soundscape Index (NSDI)
ndsi = exoacoustics.normalized_difference(data, fs)

# Write indices to a file

# Generate a cochleagram

# Plot results
