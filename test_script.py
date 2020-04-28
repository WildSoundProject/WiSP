from ecoacoustics.types import SoundRecord

# Load a sound from a wav file
filename = './audio/bird.wav'
sound_record = SoundRecord(filename)

## Calculate acoustic indices

# Acoustic Complexity Index (ACI)
# - A new methodology to infer the singing activity of an avian community: The Acoustic Complexity Index (ACI)
ACI = sound_record.acoustic_complexity

# Acoustic Diversity Index (ADI)
ADI = sound_record.acoustic_diversity

# Acoustic Evenness (AE)
AEve = sound_record.acoustic_evenness

print(f"ACI = {ACI}; ADI = {ADI}; AEve = {AEve}")

# Plot results
sound_record.plot_spectrogram(min_freq=2e3, max_freq=8e3)
