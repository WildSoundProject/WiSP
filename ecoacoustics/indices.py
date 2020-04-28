from dataclasses import dataclass
from scipy.signal import spectrogram
import numpy as np
from .utilities import gini_coefficient

# Constants
EPSILON = 1e-10


@dataclass
class SpectrogramData:
    def __init__(self, raw_samples: np.ndarray, fs: float, nfft: int = 512):
        self._duration = raw_samples.shape[0] / fs
        self._frequencies, self._times, self._values = spectrogram(raw_samples, fs=fs,
                                                                   nperseg=nfft,
                                                                   noverlap=0,
                                                                   window='hamming',
                                                                   detrend=False,
                                                                   mode='magnitude')
        # For compatibility to soundecology R package
        self._values = self._values[:-1, :]
        self._frequencies = self._frequencies[:-1]

    @property
    def values(self):
        return self._values

    @property
    def frequencies(self):
        return self._frequencies

    @property
    def times(self):
        return self._times

    @property
    def duration(self):
        return self._duration


def acoustic_complexity(spectrogram_data: SpectrogramData, j=5.0) -> float:
    # Step through the spectrogram in chunks of length j seconds
    t = spectrogram_data.times
    number_of_epochs = int(np.floor(spectrogram_data.duration / j))
    ACI_per_chunk = np.zeros(number_of_epochs)

    for i in range(number_of_epochs):
        t1 = i * j
        chunk = spectrogram_data.values[:, (t >= t1) & (t < t1 + j)]
        diffs = np.abs(chunk[:, 1:] - chunk[:, :-1])
        diff_sums = np.sum(diffs, axis=1)
        row_sums = np.sum(chunk, axis=1)
        ACI_per_chunk[i] = np.sum(diff_sums / row_sums)

    # Return the sum of ACI for each chunk
    return float(np.sum(ACI_per_chunk))


def acoustic_diversity(spectrogram_data: SpectrogramData,
                       db_threshold=-50.0,
                       maximum_frequency=10000.0,
                       frequency_step=1000.0) -> float:
    # Get the normalised spectrogram in db
    db_spectrogram = 20 * np.log10(np.clip(spectrogram_data.values, EPSILON, None) / spectrogram_data.values.max())

    # In steps of frequency_step Hz, count the proportion of spectro-temporal bins in each range of frequencies that are
    # above the threshold value
    number_of_frequency_bins = int(np.floor(maximum_frequency / frequency_step))
    f = spectrogram_data.frequencies
    proportions = np.zeros(number_of_frequency_bins)

    for i in range(number_of_frequency_bins):
        bins = db_spectrogram[(f >= i * frequency_step) & (f < (i + 1) * frequency_step), :]
        proportions[i] = np.count_nonzero(bins > db_threshold) / np.size(bins)
        proportions[i] = np.clip(proportions[i], EPSILON, None)

    # Normalise
    proportions = proportions / sum(proportions)

    return -sum(proportions * np.log2(proportions))


def acoustic_evenness(spectrogram_data: SpectrogramData,
                      db_threshold=-50.0,
                      maximum_frequency=10000.0,
                      frequency_step=1000.0) -> float:
    # Get the normalised spectrogram in db
    db_spectrogram = 20 * np.log10(np.clip(spectrogram_data.values, EPSILON, None) / spectrogram_data.values.max())

    # In steps of frequency_step Hz, count the proportion of spectro-temporal bins in each range of frequencies that are
    # above the threshold value
    number_of_frequency_bins = int(np.floor(maximum_frequency / frequency_step))
    f = spectrogram_data.frequencies
    proportions = np.zeros(number_of_frequency_bins)

    for i in range(number_of_frequency_bins):
        bins = db_spectrogram[(f >= i * frequency_step) & (f < (i + 1) * frequency_step), :]
        proportions[i] = np.count_nonzero(bins > db_threshold) / np.size(bins)

    return gini_coefficient(proportions)


def bioacoustic_index(signal: np.array, fs: float) -> float:
    pass


def acoustic_entropy(signal: np.array, fs: float) -> float:
    pass


def median_envelope(signal: np.array, fs: float) -> float:
    pass


def normalized_difference(signal: np.array, fs: float) -> float:
    pass
