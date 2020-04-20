import QtQuick 2.4
import Qt.labs.animation 1.0
import Qt.labs.calendar 1.0
import Qt.labs.settings 1.0
import Qt.labs.wavefrontmesh 1.0
import Qt.labs.qmlmodels 1.0
import Qt.labs.platform 1.1
import Qt.labs.location 1.0
import Qt.labs.folderlistmodel 2.12
import QtQuick.Controls.Material 2.0
import QtGraphicalEffects 1.0
import QtQuick.Controls 2.13

Item {
    width: 400
    height: 400

    Button {
        id: button
        x: 115
        y: 144
        text: qsTr("Button")
    }
}
