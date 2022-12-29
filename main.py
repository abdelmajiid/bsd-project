from qtpy import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt
from qtpy.QtWidgets import *
from PyQt5.QtGui import *
import sys

from BSD_UI.mainwindow import Ui_MainWindow
from BSD_UI.Client_details import Ui_Dialog
from BSD_UI.communicationWindow import Ui_MainComm


class QCustomQWidget (QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQHBoxLayout = QHBoxLayout()
        self.client_name = QLabel()
        self.button_info = QPushButton()
        self.textQHBoxLayout.addWidget(self.client_name)
        self.button_info.setText("Display info")
        self.textQHBoxLayout.addWidget(self.button_info)
        self.combobox_algo = QComboBox()
        self.combobox_algo.setMaximumWidth(120)
        self.combobox_algo.setMinimumHeight(24)
        self.textQHBoxLayout.addWidget(self.combobox_algo)
        self.button_comm = QPushButton()
        self.button_comm.setText("Communicate")
        self.textQHBoxLayout.addWidget(self.button_comm)
        self.setLayout(self.textQHBoxLayout)
        self.button_comm.setMaximumWidth(120)
        self.button_info.setMaximumWidth(120)
        # setStyleSheet
        self.client_name.setStyleSheet("margin-left:5px;\n"
"margin-right:5px;")
        self.client_name.setAlignment(Qt.AlignCenter)

        self.button_comm.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color:black;\n"
"padding: 4px;\n"
"border-radius:5px;\n"
"border-color:gray;\n"
"border-width:2px;\n"
"border-style:solid;}")
        self.button_info.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                       "color:black;\n"
                                       "padding: 4px;\n"
                                       "border-radius:5px;\n"
                                       "border-color:gray;\n"
                                       "border-width:2px;\n"
                                       "border-style:solid;}")
        self.combobox_algo.setStyleSheet("border-color:gray;\n"
"border-width:1px;\n"
"border-style:solid;\n"
"border-radius:3px;")
        self.button_info.clicked.connect(lambda: self.to_client_details(self.client_name.text()))
        self.button_comm.clicked.connect(lambda: self.communicate(self.combobox_algo.currentText(), self.client_name.text()))

    def setText(self, text):
        self.client_name.setText(text)

    def setComboBox(self, items):
        self.combobox_algo.addItems(items)

    def communicate(self, msg1, msg2):
        print("You have chose " + msg1 + " for " + msg2)
        self.close()
        self.comm_window = Communications()
        self.comm_window.show()
        self.close()

    def to_client_details(self, name):
        print("Hello " + name)
        self.details_window = ClientDetails()
        self.details_window.ui.label_prenom.setText("Prenom : " + name)
        if name == "Abdelkarim":
            nom = "Nefis"
            algo = ["RSA", "Cesar"]
        elif name == "Abdelmajid":
            nom = "Farah"
            algo = ["RSA", "viginere"]
        elif name == "Younes":
            nom = "Benlabed"
            algo = ["Cesar", "viginere", "RSA"]
        else:
            nom = "unknown"
            algo = ["void"]
        self.details_window.ui.label_nom.setText("Nom : " + nom)

        model = QtGui.QStandardItemModel()
        self.details_window.ui.listView_algo.setModel(model)
        for i in algo:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)

        self.details_window.ui.label_pic.setPixmap(QPixmap("profile.png"))
        self.details_window.ui.label_pic.setScaledContents(True)
        self.details_window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.button_scan.clicked.connect(self.displayClients)

    def displayClients(self):
        self.ui.listClients.clear()
        for name, algos in [
            ('Abdelkarim', ["RSA", "Cesar"]),
            ('Abdelmajid', ["RSA", "viginere"]),
            ('Younes', ["Cesar", "viginere", "RSA"])]:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(name)
            myQCustomQWidget.setComboBox(algos)
            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.ui.listClients)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.ui.listClients.addItem(myQListWidgetItem)
            self.ui.listClients.setItemWidget(myQListWidgetItem, myQCustomQWidget)


class ClientDetails(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class Communications(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainComm()
        self.ui.setupUi(self)
        self.ui.button_send.clicked.connect(self.send_message)
        self.ui.button_back.clicked.connect(self.back)

    def send_message(self):
        self.ui.label_server.setText(self.ui.label_server.text() + "\n" + self.ui.lineEdit.text())
        self.ui.lineEdit.clear()

    def back(self):
        self.close()
        self.mainWindow = MainWindow()
        self.mainWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




