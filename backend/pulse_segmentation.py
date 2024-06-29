import math

import numpy as np
import scipy.signal as sp_sig


class PulseSegmenter:
    """
    Helper class that performs pulse segmentation (pulse onset detection).
    """

    def __init__(self) -> None:
        """
        Initializes a Segmenter instance.
        """
        pass

    def split_pulses(self, signal: np.ndarray, time: np.ndarray, fs: float, use_mean_time: bool = False):
        """
        Splits the signal into segments corresponding to individual pulses.

        This function splits the input signal into segments corresponding to individual pulses based on the results
        of pulse onset detection. Each pulse is represented by a fragment of the signal vector and a fragment of the
        time vector (use_mean_time = False) or a single point in time corresponding to mean of the time segment
        (use_mean_time = True).

        Args:
            signal (numpy array): The one-dimensional signal vector.
            time (numpy array): The one-dimensional time vector corresponding to the signal.
            fs (float): The sampling frequency of the signal (in Hz).
            use_mean_time (bool): The flag which determines if the function should return fragments of the time
                vector (use_mean_time = False) or a single point (use_mean_time = True) for each pulse.

        Returns:
            pulses (List[numpy array]): List of segments of the signal vector corresponding to individual pulses.
            times (List[numpy array] or List[float]): List of segments of the time vector corresponding
                to individual pulses or list of mean time points for individual pulses.
            pulse_onsets (List[int]): List of indices of detected pulse onset points in the signal vector.
        """

        pulse_onsets = self._detect_pulses_in_signal(signal, fs)
        pulse_onsets = np.concatenate(([0], pulse_onsets, [len(signal) - 1]))

        pulses = [signal[pulse_onsets[i]: pulse_onsets[i + 1]] for i in range(len(pulse_onsets) - 1)]

        if use_mean_time:
            times = [np.mean(time[pulse_onsets[i]: pulse_onsets[i + 1]]) for i in range(len(pulse_onsets) - 1)]
        else:
            times = [time[pulse_onsets[i]: pulse_onsets[i + 1]] for i in range(len(pulse_onsets) - 1)]

        return pulses, times, pulse_onsets

    def _detect_pulses_in_signal(self, signal: np.ndarray, fs: float) -> np.ndarray:
        """
        Detects pulse onset points in a signal.

        This function takes a signal and its sampling frequency as input and detects the onset point for each individual
        pulse. Prior to pulse onset detection, the signal is low-pass filtered (up to 10 Hz) and detrended to improve
        accuracy.

        Args:
            signal (numpy array): The one-dimensional signal vector.
            fs (float): The sampling frequency of the signal (in Hz).

        Returns:
            numpy array: The indices of detected pulse onset points in the signal vector.
        """

        mean_signal = np.nanmean(signal)
        signal[np.argwhere(np.isnan(signal))] = mean_signal

        detrended_signal = sp_sig.detrend(signal)

        filter_critical_coefficient = 10
        filter_order = 6
        filter_max_ripple = 60
        filter_min_attenuation = 1
        filter_btype = 'lowpass'
        filter_ftype = 'cheby1'
        Wc1 = filter_critical_coefficient / fs
        b1, a1 = sp_sig.iirfilter(N=filter_order, Wn=Wc1, btype=filter_btype,
            rs=filter_max_ripple, rp=filter_min_attenuation, ftype=filter_ftype)
        filtered_signal = sp_sig.filtfilt(b1, a1, detrended_signal)

        # Note: The signal is passed to the actual detection algorithm in an inverted version so that the pulse onset
        # points are detected as maxima rather than minima (which improves accuracy). The max_scale parameter
        # is set to sampling frequency (i.e. the number of samples per second) because in humans, a pulse onset
        # is expected approximately every 0.5-1.5 seconds and max_scale limits the search range to 1 second
        # (which limits the processing time).
        signal_peaks = self._detect_peaks_troughs(-filtered_signal, max_scale=fs)
        pulse_onsets = signal_peaks[:, 0]

        return pulse_onsets

    def _detect_peaks_troughs(self, signal: np.ndarray, max_scale: float = 0) -> np.ndarray:
        """
        Detects local maxima in a signal.

        This function is the actual pulse onset detection algorithm based on the modified Scholkmann algorithm
        described in: S. M. Bishop and A. Ercole, “Multi-scale peak and trough detection optimised for periodic
        and quasi-periodic neuroscience data,” in Proc. Intracranial Press. Neuromonitoring XVI, 2018, pp. 189–195.
        This functions takes a signal and a scale value (which is approximately equivalent to the search range
        expressed in samples) as input and detects the local maxima in the signal.

        Args:
            signal (numpy array): The one-dimensional signal vector.
            max_scale (float): The maximum search range (in samples).

        Returns:
            numpy array: The indices of detected local maxima in the signal vector.
        """
        N = len(signal)
        if max_scale != 0:
            L = math.ceil(max_scale / 2) - 1
        else:
            L = math.ceil(N / 2) - 1

        detrended_signal = sp_sig.detrend(signal)

        Mx = np.zeros((N, L), dtype=np.float32)
        for kk in range(1, L + 1):
            right = detrended_signal[kk:-kk - 1] > detrended_signal[2*kk:-1]
            left = detrended_signal[kk:-kk - 1] > detrended_signal[:-2*kk-1]
            Mx[kk:-kk-1, kk-1] = np.logical_and(left, right)

        dx = np.argmax(np.sum(Mx, 0))
        Mx = Mx[:, :dx + 1]

        _, col_count = Mx.shape
        Zx = col_count - np.count_nonzero(Mx, axis=1)
        peaks = np.argwhere(Zx == 0)

        return peaks

