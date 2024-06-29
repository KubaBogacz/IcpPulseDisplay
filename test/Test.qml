import QtQuick
import QtQuick.Layouts
import QtCore

Window {
    id: root
    visible: true
    width: Screen.width/2
    height: Screen.height/2

    GridLayout {
        height: parent.height
        width: parent.width
        rows: 2
        columns: 2


        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "red"
            Layout.rowSpan: 2
            // Layout.columnSpan: 1
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "green"
            // Layout.rowSpan: 2
            // Layout.columnSpan: 2
        }


        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "blue"
            // Layout.rowSpan: 1
            // Layout.columnSpan: 1
        }
    }

}