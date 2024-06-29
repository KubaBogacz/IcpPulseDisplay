import QtCore
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 1024
    height: 768
    title: qsTr("Plotter")
    visible: true

    // Name of provided data i.e. name of folder with data
    property string fileName

    // Initialisation of window to select data
    SelectDialogWindow {
        id: selectDialogWindow
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
    }

    // Menu bar on the top of program
    menuBar: MenuBar {
        Menu {
            title: qsTr("&File")

            MenuItem {
                text: qsTr("&Open...")
                icon.name: "document-open"
                onTriggered: {
                    CustomChart.holdOn = false;
                    selectDialogWindow.open();
                }
            }

            MenuItem {
                text: qsTr("&Save")
                icon.name: "document-save"
                //TODO: Make the file name description more precise by adding more data to function
                onTriggered: saveChart(root.fileName + ".png")
            }

            MenuItem {
                text: qsTr("Save &As...")
                icon.name: "document-save-as"
            }

            MenuItem {
                text: qsTr("Add new series")
                icon.name: "list-add"
                onTriggered: {
                    chart.holdOn = true;
                    fileOpenDialog.open();
                }
            }
        }

        Menu {
            title: qsTr("&Help")
            MenuItem {
                text: qsTr("&About...")
                onTriggered: aboutDialog.open()
            }
        }
    }

    // File dialog to open .csv files
    FileDialog {
        id: fileOpenDialog
        title: "File dialog"
        currentFolder: StandardPaths.standardLocations(StandardPaths.HomeLocation)[0]
        nameFilters: ["CSV files (*.csv)"]
        onAccepted: {
            var path = selectedFile.toString();
            // Unix
            // path = path.replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/,"/");;
            // Windows
            path = path.replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/,"");
            chart.newData(path, selectDialogWindow.columnLabels);
        }
    }

    // Dialog which provides informations about program
    Dialog {
        id: aboutDialog
        width: 300
        height: 200
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        modal: false
        standardButtons: Dialog.Ok

        header: ToolBar {
            background: Rectangle {
                color: "#6e6e6e"
                radius: 2
            }
            RowLayout {
                anchors.fill: parent
                Label {
                    text: "About"
                    elide: Label.ElideRight
                    horizontalAlignment: Qt.AlignHCenter
                    verticalAlignment: Qt.AlignVCenter
                    Layout.fillWidth: true
                }
                ToolButton {
                    text: qsTr("x")
                    onClicked: aboutDialog.close()
                }
            }
        }

        Label {
            text: "Lorem ipsum..."
            anchors.fill: parent
        }
    }


    GridLayout {
        id: mainGrid
        anchors.fill: parent

        columns: 2
        rows: 2

        CustomChart {
            id: chart
            Layout.fillHeight: true
            Layout.minimumHeight: 300
            Layout.preferredWidth: parent.width * 0.65
            Layout.minimumWidth: 400
            Layout.rowSpan: 2

            onUpdated: (seriesName, seriesColor) => {
                root.fileName = seriesName;
                basicInfo.fileName = seriesName;
                basicInfo.samplingFrequency
            }
        }

        BasicInfo {
            id: basicInfo
            Layout.preferredHeight: 50
            Layout.fillWidth: true
            Layout.topMargin: 10
            Layout.rightMargin: 10
        }

        // PeakDataContainer {
        //     id: peakDataContainer
        //     Layout.fillHeight: true
        //     Layout.fillWidth: true
        //     Layout.topMargin: 5
        //     Layout.bottomMargin: 10
        //     Layout.rightMargin: 10
        // }


        
    }
}
