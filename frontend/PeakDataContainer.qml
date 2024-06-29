import QtQuick

Rectangle {
    id: root
    radius: 5

    property real peakMean: 0
    property real peakAmplitude: 0
    property real peakSlope: 0
    property real peakClass: 0

    Text {
        id: peakClassText
        anchors.top: parent.top
        anchors.left: parent.left
        padding: 5

        text: qsTr("Peak class: ") + backend.peakClass
    }

    Text {
        id: peakMeanText
        anchors.top: peakClassText.bottom
        anchors.left: parent.left
        padding: 5

        text: qsTr("Mean: ") + backend.peakClass
    }

    Text {
        id: peakAmplitudeText
        anchors.top: peakMeanText.bottom
        anchors.left: parent.left
        padding: 5

        text: qsTr("Amplitude: ") + backend.peakAmplitude
    }

    Text {
        id: peakSlopeText
        anchors.top: peakAmplitudeText.bottom
        anchors.left: parent.left
        padding: 5

        text: qsTr("Slope: ") + backend.peakSlope
    }
}
