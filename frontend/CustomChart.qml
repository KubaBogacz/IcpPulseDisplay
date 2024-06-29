import QtQuick
import QtCharts
import Plotter 1.0

// Plot made in ChartView window
ChartView {
    id: root
    antialiasing: true
    legend.visible: false
    title: " "

    // Signal is emitted when object finishes adding new series (updating plot)
    signal updated(string seriesName, color seriesColor)

    // Signal is emitted when new data is added
    signal newData(string fileUrl)

    // Holds on plot like Matlab
    property bool holdOn

    Plotter {
        id: plotter
    }

    ValueAxis {
        id: myAxisX
        titleText: "t [s]"
    }

    ValueAxis {
        id: myAxisY
        titleText: "y"
    }

    // Executes when program finishes creating ChartView object on startup
    // Adds a series so that the window is not empty
    Component.onCompleted: {
        var empty = root.createSeries(ChartView.SeriesTypeLine, "line", myAxisX, myAxisY)
    }

    Connections {
        target: root
        // When new data is provided
        function onNewData(fileUrl, columnLabels) {

            // If hold on is off clears the entire object and series
            if (!holdOn) {
                root.removeAllSeries()
                plotter.clearObject()
            }

            // Adds data if it does not exists yet
            if (!plotter.isFile(fileUrl)) {
                // Crates series
                plotter.initialize(fileUrl, columnLabels)
                var abp = root.createSeries(ChartView.SeriesTypeLine, "abp", myAxisX, myAxisY)
                var icp = root.createSeries(ChartView.SeriesTypeLine, "icp", myAxisX, myAxisY)
                var fvl = root.createSeries(ChartView.SeriesTypeLine, "fvl", myAxisX, myAxisY);
                var fvr = root.createSeries(ChartView.SeriesTypeLine, "fvr", myAxisX, myAxisY);

                // Fill series and set axes limits
                plotter.fillSeries(abp, icp, fvl, fvr)
                plotter.setAxes(myAxisX, myAxisY)


                var fileName = fileUrl.substring(0, fileUrl.length - 4).replace(/^.*[\\/]/, '')

                // Sets color and name
                //var color = line.color
                root.updated(fileName, color)
            }
        }
    }

    // Mask to scroll plot
    Rectangle {
        id: scrollMask
        visible: false
        x: 0
        property int currentX: 0
        property int scrolls: 0
    }

    // It is necessary to control it with mouse
    MouseArea {
        id: chartMouseArea
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton
        onDoubleClicked: plotter.setAxes(myAxisX, myAxisY)

        // Scroll horizontally
        onMouseXChanged: mouse => {
                             if ((mouse.buttons & Qt.LeftButton) == Qt.LeftButton) {
                                root.scrollLeft(mouseX - scrollMask.x)
                                scrollMask.currentX -= mouseX - scrollMask.x;
                                scrollMask.x = mouseX
                                // console.log(scrollMask.currentX * 2**(Math.abs(scrollMask.scrolls)) / 544)
                                console.log(scrollMask.currentX * 2**(scrollMask.scrolls)) / 544
                             }
                         }

        // Scroll vertically
        onMouseYChanged: mouse => {
                             if ((mouse.buttons & Qt.LeftButton) == Qt.LeftButton) {
                                 root.scrollUp(mouseY - scrollMask.y)
                                 scrollMask.y = mouseY
                             }
                         }

        // Sets scroll properties to current mouse position
        onPressed: mouse => {
                       if (mouse.button === Qt.LeftButton) {
                           scrollMask.x = mouseX
                           scrollMask.y = mouseY
                       }
                   }

        // Zoom on wheel
        onWheel: wheel => {
                     if (wheel.angleDelta.y > 0) {
                        root.zoomIn()
                        scrollMask.scrolls--
                     } else {
                        scrollMask.scrolls++
                        root.zoomOut()
                     }
                     console.log((scrollMask.currentX * 2**scrollMask.scrolls) / 544)
                 }
    }
}
