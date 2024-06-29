from pathlib import Path

import numpy as np
import pandas as pd

from backend.signal_processing import convert_datetime_to_time, filter_signal

from backend.pulse_segmentation import PulseSegmenter
from backend.basic_pulse_analysis import BasicPulseAnalyzer
from backend.pulse_classification import PulseClassifier

import matplotlib.pyplot as plt


segmenter = PulseSegmenter()
basic_analyzer = BasicPulseAnalyzer()
classifier = PulseClassifier()


file_path = Path(r'E:\\_BrainLab\\SampleRecords\\testowy_bardzo_krotki.csv')
with open(file_path, 'r') as f:
    data = pd.read_csv(f)
datetime = data['DateTime'].to_numpy()
icp = data['icp[mmHg]'].to_numpy()

# convert timestamps to time in seconds and estimate sampling frequency
time, fs = convert_datetime_to_time(datetime)

# filter the signal
icp = filter_signal(icp, fs)

# segment the signal (divide the signal in individual pulses)
segments, times, _ = segmenter.split_pulses(icp, time, fs)
mean_times = [np.mean(pulse_time) for pulse_time in times]

# calculate basic pulse metrics
pulse_means = basic_analyzer.batch_calculate_pulse_mean(segments)
pulse_amplitudes = basic_analyzer.batch_calculate_pulse_amplitude(segments)
pulse_slopes = basic_analyzer.batch_calculate_pulse_slope(segments, times)

# classify the pulses using a neural network model; classes 1-4 are valid shapes and class 5 are artifacts
pulse_classes = classifier.classify_batch(segments)

print(type(time))
print(type(fs))
