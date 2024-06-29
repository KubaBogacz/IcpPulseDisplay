from PySide6.QtCore import QObject, Signal, Property

class Backend(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._class = 1
        self._mean = 12.1
        self._amplitude = 13.2
        self._slope = 14.3

    def _get_class(self):
        return self._class
    
    def _set_class(self, val):
        if self._class != val:
            self._class = val
            self.classChanged.emit()
    
    def _get_mean(self):
        return self._mean
    
    def _set_mean(self, val):
        if self._mean != val:
            self._mean = val
            self.meanChanged.emit()
    
    def _get_amplitude(self):
        return self._amplitude
    
    def _set_amplitude(self, val):
        if self._amplitude != val:
            self._amplitude = val
            self.amplitudeChanged.emit()
    
    def _get_slope(self):
        return self._slope
    
    def _set_slope(self, val):
        if self._slope != val:
            self._slope = val
            self.slopeChanged.emit()
            
    classChanged = Signal()
    meanChanged = Signal()
    amplitudeChanged = Signal()
    slopeChanged = Signal()

    peakClass = Property(int, _get_class, _set_class, notify=classChanged)
    peakMean = Property(float, _get_mean, _set_mean, notify=meanChanged)
    peakAmplitude = Property(float, _get_amplitude, _set_amplitude, notify=amplitudeChanged)
    peakSlope = Property(float, _get_slope, _set_slope, notify=slopeChanged)