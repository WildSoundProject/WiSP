import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram


def acoustic_complexity(filename: str, j=5.0, nfft=512) -> float:

    # Read the audio file
    fs, data = wavfile.read(filename)

    # Calculate the spectrogram
    f, t, Sxx = spectrogram(data, fs=fs,
                     nperseg=nfft,
                     noverlap=0,
                     window='hamming',
                     detrend=False,
                     mode='magnitude')

    # For compatibility with Soundecology R package, remove last frequency bin
    # Numbers may still differ marginally due to FFT implementations
    Sxx = Sxx[:-1, :]
    f = f[:-1]

    # Step through the spectrogram in chunks of length j seconds
    duration = len(data) / fs
    number_of_epochs = int(np.floor(duration / j))
    ACI_per_chunk = np.zeros(number_of_epochs)

    for i in range(number_of_epochs):
        t1 = i * j
        chunk = Sxx[:, (t >= t1) & (t < t1 + j)]
        diffs = np.abs(chunk[:, 1:] - chunk[:, :-1])
        diff_sums = np.sum(diffs, axis=1)
        row_sums = np.sum(chunk, axis=1)
        ACI_per_chunk[i] = np.sum(diff_sums / row_sums)

    # Return the sum of ACI for each chunk
    return float(np.sum(ACI_per_chunk))


def acoustic_diversity(filename: str, j=5.0, nfft=512) -> float:
    
    pass


def acoustic_evenness(signal: np.array, fs: float) -> float:
    pass


def bioacoustic_index(signal: np.array, fs: float) -> float:
    pass


def acoustic_entropy(signal: np.array, fs: float) -> float:
    pass


def median_envelope(signal: np.array, fs: float) -> float:
    pass


def normalized_difference(signal: np.array, fs: float) -> float:
    pass