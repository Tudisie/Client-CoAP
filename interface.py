from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QDesktopWidget, QLineEdit, QPlainTextEdit
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QFont

from header import *
from functions import *
from receiver import *
import receiver

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "CoAP Client"
        self.width = 480
        self.height = 800

        self.connectedToServer = False

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.center()

        self.timerButtonDisabled = 0
        self.timer = QTimer(self)
        #adding action to timer
        self.timer.timeout.connect(self.counter)
        #updating the timer every 100ms
        self.timer.start(100)

        #Connect to The Server Button
        self.connectButton = QPushButton("Connect", self)
        self.connectButton.move(50, 200)
        self.connectButton.setCheckable(True)
        self.connectButton.clicked.connect(self.button_clicked_connectServer)

        #Send Package Button
        self.sendButton = QPushButton("Send Package", self)
        self.sendButton.move(50, 280)
        self.sendButton.setCheckable(True)
        self.sendButton.clicked.connect(self.button_clicked_sendPackage)

        #input text boxes
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(16)

        self.label1 = QLabel(self)
        self.label1.setText("dest. IP:")
        self.label1.move(20,20)

        self.dip = QLineEdit(self)
        self.dip.move(85,20)
        self.dip.resize(130,30)
        self.dip.setText("192.168.43.89")


        self.label2 = QLabel(self)
        self.label2.setText("src. port:")
        self.label2.move(20, 60)

        self.sport = QLineEdit(self)
        self.sport.move(85, 60)
        self.sport.resize(130, 30)
        self.sport.setText("10001")


        self.label3 = QLabel(self)
        self.label3.setText("dest. port:")
        self.label3.move(20, 100)

        self.dport = QLineEdit(self)
        self.dport.move(85, 100)
        self.dport.resize(130, 30)
        self.dport.setText("10010")

        #Console Outputs
        self.plainText = QPlainTextEdit()
        self.plainText.setReadOnly(True)
        self.plainText.setFixedWidth(self.width - 40)
        self.plainText.setFixedHeight(180)
        #self.plainText.move(0,0)

        self.plainText.appendPlainText("Command Prompt!")

        layout = QVBoxLayout()
        layout.addWidget(self.plainText)
        self.setLayout(layout)

        self.show()

    def button_clicked_sendPackage(self):
        global s
        self.timerButtonDisabled = 10
        headerString = createHeader()

        # Sending the packet to the server:
        receiver.s.sendto(bytes(headerString, encoding="utf-8"), (str(self.dip.text()), int(self.dport.text())))

    def button_clicked_connectServer(self):
        if self.connectedToServer == False:
            #check the DIP format
            failure = False
            if isValidIP(self.dip.text()) == False:
                self.plainText.appendPlainText("Invalid format for DIP")
                failure = True
            if isValidPort(1053) == False:
                self.plainText.appendPlainText("Violation of Reserved Port")
                failure = True
            if failure == False:
                self.connectedToServer = True
                self.plainText.appendPlainText("Connected to the server")
                create_socket(self.sport.text())
            else:
                self.plainText.appendPlainText("Failed to connect to the server")
        else:
            self.plainText.appendPlainText("Already connected to a server!")


    def counter(self):
        if self.timerButtonDisabled:
            self.timerButtonDisabled -= 1
            self.sendButton.setEnabled(False)
        else:
            self.sendButton.setEnabled(True)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())