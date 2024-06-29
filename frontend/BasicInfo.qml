import QtQuick

Item {
    id: basicInfo
    visible: true

    // Name of provided data i.e. name of folder with data
    property string fileName: qsTr("No file selected")

    // Estimated sampling frequency of data
    property real samplingFrequency: 0

    Row {
        id: basicInfoRow
        anchors.fill: parent
        spacing: 5

        Rectangle {
            id: fileNameRectangle
            height: basicInfoRow.height
            width: basicInfoRow.width / 2
            color: "white"
            radius: 5


            Column {
                Text {
                    id: text1
                    padding: 5
                    text: qsTr("File: ")
                    font.bold: true
                    font.pixelSize: 12
                }

                Text {
                    id: text2
                    padding: 5
                    topPadding: 0
                    text: basicInfo.fileName
                    font.pixelSize: 12
                }
            }
        }

        Rectangle {
            id: estimatedFsRectangle
            height: basicInfoRow.height
            width: basicInfoRow.width / 2 - 5
            color: "white"
            visible: true
            radius: 5

           Column {
                Text {
                    id: text3
                    padding: 5
                    text: qsTr("Sampling frequency: ")
                    font.bold: true
                    font.pixelSize: 12
                }

                Text {
                    id: text4
                    padding: 5
                    topPadding: 0
                    text: basicInfo.samplingFrequency + " Hz"
                    font.pixelSize: 12
                }
           }
        }
    }
}