import QtQuick 2.15
import QtQuick.Controls 2.15
import Controller 1.0

Dialog {
    id: root
    width: 180
    height: 200
    modal: true
    closePolicy: Dialog.CloseOnEscape

    property list<bool> columnLabels: [true, false, false, false];

    Controller {
        id: controller
    }

    Column {
        anchors.centerIn: parent
        spacing: 10
        padding: 10

        Label {
            text: "Select"
            font.pixelSize: 20
        }

        CheckBox {
            id: icpCheckBox
            checked: true
            text: "icp[mmHg]"
            onCheckedChanged: {
                if (checkState == Qt.Checked) {
                    columnLabels[0] = true;
                } else {
                    columnLabels[0] = false;
                }
            }
        }

        CheckBox {
            id: abpCheckBox
            text: "abp[mmHg]"
            onCheckedChanged: {
                if (checkState == Qt.Checked) {
                    columnLabels[1] = true;
                } else {
                    columnLabels[1] = false;
                }
            }
        }

        CheckBox {
            id: fvlCheckBox
            text: "fvl[cm/s]"
            onCheckedChanged: {
                if (checkState == Qt.Checked) {
                    columnLabels[2] = true;
                } else {
                    columnLabels[2] = false;
                }
            }
        }

        CheckBox {
            id: fvrCheckBox
            text: "fvr[cm/s]"
            onCheckedChanged: {
                if (checkState == Qt.Checked) {
                    columnLabels[3] = true;
                } else {
                    columnLabels[3] = false;
                }
            }
        }

        Button {
            text: "Select Data"
            onClicked: {
                root.close()
                fileOpenDialog.open();
                controller.newColumnLabels(columnLabels)
            }
        }
    }
}
