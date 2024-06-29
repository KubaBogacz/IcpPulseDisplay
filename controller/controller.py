from backend.pulse_segmentation import PulseSegmenter
from backend.basic_pulse_analysis import BasicPulseAnalyzer
from backend.pulse_classification import PulseClassifier
from backend.signal_processing import convert_datetime_to_time
from test.utils import Utils

from PySide6.QtCore import QObject, Slot, Signal

import polars as pl
import numpy as np

segmenter = PulseSegmenter()
basic_analyzer = BasicPulseAnalyzer()
classifier = PulseClassifier()

class Controller(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.columnLabels = []
        print("Column labels in __init__: ")
        print(self.columnLabels)
    
    
    @Slot(list)
    def newColumnLabels(self, dataColumns):
        columnLabels = []

        for index, label in enumerate(dataColumns):
            if label:
                if index == 0:
                    columnLabels.append("abp")
                elif index == 1:
                    columnLabels.append("icp")
                elif index == 2:
                    columnLabels.append("fvl")
                elif index == 3:
                    columnLabels.append("fvr")
                else:
                    print("No such column in dataColumns")

        self.columnLabels = columnLabels
        print("Column labels in newColumnLabels: ")
        print(self.columnLabels)


    def read_column_labels(self):
        print("Column labels in read_column_labels: ")
        print(self.columnLabels)
        return self.columnLabels



    




