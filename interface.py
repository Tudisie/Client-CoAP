from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QPushButton, QVBoxLayout, QDesktopWidget, QLineEdit, QGridLayout, QPlainTextEdit, QWidget, QLabel
from PyQt5.QtCore import QTimer
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


        self.sendButton = QPushButton("Send Package", self)
        self.sendButton.clicked.connect(self.button_clicked_sendPackage)

        #Connection Layout

        self.label1 = QLabel("dest. IP:", self)
        self.dip = QLineEdit("192.168.1.106", self)

        self.label2 = QLabel("src. port:", self)
        self.sport = QLineEdit("10001", self)

        self.label3 = QLabel("dest. port:", self)
        self.dport = QLineEdit("10010",self)

        self.connectButton = QPushButton("Connect", self)
        self.connectButton.clicked.connect(self.button_clicked_connectServer)

        grid1 = QGridLayout()
        grid1.setSpacing(10)
        grid1.addWidget(self.label1, 1, 0)
        grid1.addWidget(self.dip, 1, 1)
        grid1.addWidget(self.label2, 2, 0)
        grid1.addWidget(self.sport, 2, 1)
        grid1.addWidget(self.label3, 3, 0)
        grid1.addWidget(self.dport, 3, 1)
        grid1.addWidget(self.connectButton, 4, 0, 1, 2)

        #Sending Package Layout

        self.labelCommand = QLabel("Command:", self)
        self.command = QLineEdit(self)

        grid2 = QGridLayout()
        grid2.addWidget(self.labelCommand, 1, 0)
        grid2.addWidget(self.command, 1, 1)
        grid2.addWidget(self.sendButton, 2, 0, 1, 2)

        vbox = QVBoxLayout()
        vbox.addLayout(grid1)
        vbox.addLayout(grid2)

        #Console Outputs
        self.plainText = QPlainTextEdit()
        self.plainText.setReadOnly(True)
        self.plainText.setFixedHeight(200)
        self.plainText.appendPlainText("Command Prompt!")

        vbox.addWidget(self.plainText)

        self.setLayout(vbox)

        self.show()

    def button_clicked_sendPackage(self):
        global s
        self.timerButtonDisabled = 10
        headerString = createHeader("Tudisika", "noParolo", self.command.text())

        # Sending the packet to the server:
        bytesToSend = bytes(headerString, encoding="latin_1")
        receiver.s.sendto(bytesToSend, (str(self.dip.text()), int(self.dport.text())))

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