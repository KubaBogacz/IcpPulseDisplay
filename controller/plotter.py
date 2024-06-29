import polars as pl
import time
import numpy as np

from backend.signal_processing import convert_datetime_to_time

from PySide6.QtCore import  QObject, QPointF, Slot, Signal
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis

class Plotter(QObject):
    # Limit values
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    values = dict.fromkeys(["time", "abp", "icp", "fvl", "fvr"])
    valuesLen = 0

    # Names of .csv files
    fileNames = []

    # Data column labels
    columnLabels = []

    time = np.ndarray([])
    fs = np.float64()

    def new_column_labels(dataColumns):
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

        return columnLabels
        
    # Fills plot with provided fillSeries
    @Slot(str)
    def initialize(self, path, columnLabels):
        self.fileNames.append(path)
        df = pl.read_csv(path)
        self.time, self.fs = convert_datetime_to_time(df.get_column("DateTime").to_numpy())
        self.columnLabels = self.new_column_labels(columnLabels)
        print("Column labels in plot: ")
        print(self.columnLabels)



        # self.values["time"] = self.time
        # if "icp" in self.columnLabels:
        #     self.values["icp"] = df.get_column("icp[mmHg]")
        # if "abp" in self.columnLabels:
        #     self.values["abp"] = df.get_column("abp[mmHg]")
        # if "fvl" in self.columnLabels:
        #     self.values["fvl"] = df.get_column("fvl[cm/s]")
        # if "fvr" in self.columnLabels:
        #     self.values["fvr"] = df.get_column("fvr[cm/s]")
        # if not self.columnLabels:
        #     print("columnLabels is empty")
        self.valuesLen = len(self.values["time"])

        self.vals_range = [0, self.valuesLen]

    @Slot(QLineSeries, QLineSeries, QLineSeries, QLineSeries, result=None)
    def fillSeries(self, abp, icp, fvl, fvr):

        if "icp" in self.values:
            icp_points = [QPointF(x, y) for x, y in zip(self.values["time"][self.vals_range[0]:self.vals_range[1]], self.values["icp"][self.vals_range[0]:self.vals_range[-1]])]
            icp.append(icp_points)

        if "abp" in self.values:
            abp_points = [QPointF(x, y) for x, y in zip(self.values["time"][self.vals_range[0]:self.vals_range[1]], self.values["abp"][self.vals_range[0]:self.vals_range[-1]])]
            abp.append(abp_points)

        if "fvl" in self.values:
            fvl_points = [QPointF(x, y) for x, y in zip(self.values["time"][self.vals_range[0]:self.vals_range[1]], self.values["fvl"][self.vals_range[0]:self.vals_range[-1]])]
            fvl.append(fvl_points)

        if "fvr" in self.values:
            fvr_points = [QPointF(x, y) for x, y in zip(self.values["time"][self.vals_range[0]:self.vals_range[1]], self.values["fvr"][self.vals_range[0]:self.vals_range[-1]])]
            fvr.append(fvr_points)
        
        # Calculate time of execution
        start_time = time.time()
        print("--- %s seconds ---" % (time.time() - start_time))



    # Sets axes limits
    # Objects contains current limits and compares it with new ones
    @Slot(QValueAxis, QValueAxis)
    def setAxes(self, xAxis, yAxis):
        minX = min(self.values["time"][self.vals_range[0]:self.vals_range[-1]])
        maxX = max(self.values["time"][self.vals_range[0]:self.vals_range[-1]])
        minY = min(self.values["icp"][self.vals_range[0]:self.vals_range[-1]])
        maxY = max(self.values["icp"][self.vals_range[0]:self.vals_range[-1]])

        self.minX = minX if minX < self.minX else self.minX
        self.maxX = maxX if maxX > self.maxX else self.maxX
        self.minY = minY if minY < self.minY else self.minY
        self.maxY = maxY if maxY > self.maxY else self.maxY

        minX  = self.minX - abs(self.maxX - self.minX) * 0.2
        maxX  = self.maxX + abs(self.maxX - self.minX) * 0.2
        minY  = self.minY - abs(self.maxY - self.minY) * 0.2
        maxY  = self.maxY + abs(self.maxY - self.minY) * 0.2

        xAxis.setProperty('min', minX)
        xAxis.setProperty('max', maxX)
        yAxis.setProperty('min', minY)
        yAxis.setProperty('max', maxY)

    # Clears current Plotter object
    @Slot()
    def clearObject(self):
        # Limit values
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        self.values = dict.fromkeys(["time", "abp", "icp", "fvl", "fvr"])
        self.valuesLen = 0

        # Names of .csv files
        self.fileNames = []

    # Checks if the file was already provided
    @Slot(str, result=bool)
    def isFile(self, path):
        return path in self.fileNames
