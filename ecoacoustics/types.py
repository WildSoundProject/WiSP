from scipy.io import wavfile
from .indices import *
from typing import Tuple
import matplotlib.pyplot as plt


@dataclass
class SoundRecord:

    def __init__(self, filename: str):
        self._spectrogram_data = None
        self._acoustic_complexity = None
        self._acoustic_diversity = None
        self._acoustic_evenness = None

        # Try to read the file
        try:
            self._fs, self._raw_samples = wavfile.read(filename)
        except IOError:
            print("Error reading .wav file. unable to create sound record.")

        self._duration = self._raw_samples.shape[0] / self._fs

        # Save the name of the file
        self._filename = filename

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def raw_samples(self) -> np.ndarray:
        return self._raw_samples

    @property
    def fs(self) -> float:
        return self._fs

    @property
    def number_of_channels(self) -> int:
        return 1 if self._raw_samples.ndim == 1 else self._raw_samples.shape[1]

    @property
    def spectrogram_data(self) -> SpectrogramData:
        if self._spectrogram_data is None:
            self._spectrogram_data = SpectrogramData(self._raw_samples, self._fs)

        return self._spectrogram_data

    @property
    def acoustic_complexity(self) -> float:
        if self._acoustic_complexity is None:
            self._acoustic_complexity = acoustic_complexity(self.spectrogram_data)

        return self._acoustic_complexity

    @property
    def acoustic_diversity(self) -> float:
        if self._acoustic_diversity is None:
            self._acoustic_diversity = acoustic_diversity(self.spectrogram_data)

        return self._acoustic_diversity

    @property
    def acoustic_evenness(self) -> float:
        if self._acoustic_evenness is None:
            self._acoustic_evenness = acoustic_evenness(self.spectrogram_data)

        return self._acoustic_evenness


    def plot_spectrogram(self, min_freq=0.0, max_freq=10.0e3) -> None:
        if self._spectrogram_data is None:
            self._spectrogram_data = SpectrogramData(self._raw_samples, self._fs)

        values = self._spectrogram_data.values
        f = self._spectrogram_data.frequencies
        db_spectrogram = 20 * np.log10(np.clip(values, EPSILON, None) / values.max())
        plt.imshow(db_spectrogram[(f > min_freq) & (f < max_freq), :],
                   origin='lower',
                   aspect='auto',
                   extent=[0.0, self._duration, min_freq, max_freq],
                   cmap=plt.get_cmap("Greys"),
                   vmin=-50)
        plt.show()
