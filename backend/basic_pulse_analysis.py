from typing import List

import numpy as np


class BasicPulseAnalyzer:
    """
    Helper class that calculates basic pulse metrics.
    """

    def __init__(self) -> None:
        """
        Initializes a BasicPulseAnalyzer instance.
        """
        pass

    def calculate_pulse_mean(self, pulse: np.ndarray) -> float:
        """
        Calculates the mean value of a single pulse.

        Args:
            pulse (numpy array): The one-dimensional pulse vector.

        Returns:
            float: The calculated mean value.
        """
        return np.nanmean(pulse)

    def batch_calculate_pulse_mean(self, pulses: List[np.ndarray]) -> List[float]:
        """
        Batch version of mean value calculations.

        Args:
            pulses (List[numpy array]): List of one-dimensional vectors corresponding to individual pulses.

        Returns:
            List[float]: List of mean values calculated for individual pulses.
        """
        means = [self.calculate_pulse_mean(pulse) for pulse in pulses]
        return means

    def calculate_pulse_amplitude(self, pulse: np.ndarray) -> float:
        """
        Calculates the peak-to-peak amplitude of a single pulse, defined as max - min value of the pulse.

        Args:
            pulse (numpy array): The one-dimensional pulse vector.

        Returns:
            float: The calculated pulse amplitude.
        """
        if not np.all(np.isnan(pulse)) and np.nanmax(pulse) != np.nanmin(pulse):
            return np.nanmax(pulse) - np.nanmin(pulse)
        else:
            return np.nan

    def batch_calculate_pulse_amplitude(self, pulses: List[np.ndarray]) -> List[float]:
        """
        Batch version of pulse amplitude calculations.

        Args:
            pulses (List[numpy array]): List of one-dimensional vectors corresponding to individual pulses.

        Returns:
            List[float]: List of pulse amplitudes calculated for individual pulses.
        """
        amplitudes = [self.calculate_pulse_amplitude(pulse) for pulse in pulses]
        return amplitudes

    def calculate_pulse_slope(self,  pulse: np.ndarray, time: np.ndarray) -> float:
        """
        Calculates the ascending slope of a single pulse, defined as the change in the signal (d_pulse) over the change
        in time (d_t) from pulse onset to pulse maximum.

        Args:
            pulse (numpy array): The one-dimensional pulse vector.

        Returns:
            float: The calculated pulse slope.
        """
        pulse_max = np.argmax(pulse)
        d_t = time[pulse_max] - time[0]
        d_pulse = pulse[pulse_max] - pulse[0]
        if d_t != 0:
            return d_pulse / d_t
        else:
            return np.nan

    def batch_calculate_pulse_slope(self, pulses: List[np.ndarray], times: List[np.ndarray]) -> List[float]:
        """
        Batch version of pulse slope calculations.

        Args:
            pulses (List[numpy array]): List of one-dimensional vectors corresponding to individual pulses.

        Returns:
            List[float]: List of pulse slopes calculated for individual pulses.
        """
        slopes = [self.calculate_pulse_slope(pulse, time) for pulse, time in zip(pulses, times)]
        return slopes

