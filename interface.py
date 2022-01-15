from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from header import *
from functions import *
import receiver

commandList = ["cd", "ls", "pwd", "msg", "readText", "run", "newFile", "newDir", "rm", "copy", "paste", "write",
               "append"]
commandInfo = [
    ".. / PATH",
    "",
    "",
    "\t      [text]",
    "filename.ext",
    "filename.exe",
    "filename.ext",
    "dirname",
    "filename.ext / dirname",
    "filename.ext",
    "",
    "filename.ext      [text]",
    "filename.ext      [text]",
]


class MainWindow(object):
    def __init__(self, dialog):
        self.initUI(dialog)

        # Timer
        self.timer = QTimer()
        # adding action to timer
        self.timer.timeout.connect(self.counter)
        # updating the timer every 100ms
        self.timer.start(100)

        # Variables
        self.connectedToServer = False
        self.input_destPort.setText('10010')
        self.input_srcPort.setText('10001')
        self.input_destIP.setText('192.168.1.109')
        self.input_username.setText('tudisie')
        self.input_password.setText('matiz4life')
        self.userID = ""
        self.password = ""

        # Connecting controls to functions
        self.button_connect.clicked.connect(self.ConnectToServer)
        self.button_register.clicked.connect(self.Register)
        self.button_login.clicked.connect(self.Login)
        self.button_sendPackage.clicked.connect(self.SendPackage)
        self.button_clearCmd.clicked.connect(self.ClearCommandPrompt)
        self.button_clearResponse.clicked.connect(self.ClearResponse)
        self.button_displayAllCommands.clicked.connect(self.DisplayAllCommands)

        self.input_command.returnPressed.connect(self.button_sendPackage.click)
        self.input_username.returnPressed.connect(self.button_login.click)
        self.input_password.returnPressed.connect(self.button_login.click)
        self.input_destIP.returnPressed.connect(self.button_connect.click)
        self.input_srcPort.returnPressed.connect(self.button_connect.click)
        self.input_destPort.returnPressed.connect(self.button_connect.click)

    def initUI(self, dialog):
        font9 = QtGui.QFont()
        font9.setPointSize(9)
        font10 = QtGui.QFont()
        font10.setPointSize(10)

        dialog.setObjectName("dialog")
        dialog.resize(640, 755)
        self.groupBoxServerConnection = QtWidgets.QGroupBox(dialog)
        self.groupBoxServerConnection.setGeometry(QtCore.QRect(10, 20, 311, 211))
        self.groupBoxServerConnection.setFont(font9)
        self.groupBoxServerConnection.setObjectName("groupBoxServerConnection")
        self.groupBoxResponse = QtWidgets.QGroupBox(dialog)
        self.groupBoxResponse.setGeometry(QtCore.QRect(330, 330, 301, 421))
        self.groupBoxResponse.setFont(font9)
        self.groupBoxResponse.setObjectName("groupBoxResponse")
        self.console_response = QtWidgets.QTextBrowser(self.groupBoxResponse)
        self.console_response.setGeometry(QtCore.QRect(10, 30, 281, 341))
        self.console_response.setObjectName("console_response")
        self.button_clearResponse = QtWidgets.QPushButton(self.groupBoxResponse)
        self.button_clearResponse.setGeometry(QtCore.QRect(10, 380, 281, 28))
        self.button_clearResponse.setFont(font10)
        self.button_clearResponse.setObjectName("button_clearResponse")
        self.groupBoxSignIn = QtWidgets.QGroupBox(dialog)
        self.groupBoxSignIn.setGeometry(QtCore.QRect(10, 240, 311, 211))
        self.groupBoxSignIn.setFont(font9)
        self.groupBoxSignIn.setObjectName("groupBoxSignIn")
        self.label_command = QtWidgets.QLabel(dialog)
        self.label_command.setGeometry(QtCore.QRect(340, 60, 81, 21))
        self.label_command.setFont(font10)
        self.label_command.setObjectName("label_command")
        self.label_destPort = QtWidgets.QLabel(dialog)
        self.label_destPort.setGeometry(QtCore.QRect(30, 140, 81, 21))
        self.label_destPort.setFont(font10)
        self.label_destPort.setObjectName("label_destPort")
        self.input_destPort = QtWidgets.QLineEdit(dialog)
        self.input_destPort.setGeometry(QtCore.QRect(120, 140, 191, 22))
        self.input_destPort.setFont(font10)
        self.input_destPort.setObjectName("input_destPort")
        self.label_password = QtWidgets.QLabel(dialog)
        self.label_password.setGeometry(QtCore.QRect(30, 320, 91, 21))
        self.label_password.setFont(font10)
        self.label_password.setObjectName("label_password")
        self.label_destIP = QtWidgets.QLabel(dialog)
        self.label_destIP.setGeometry(QtCore.QRect(30, 60, 81, 21))
        self.label_destIP.setFont(font10)
        self.label_destIP.setObjectName("label_destIP")
        self.label_msgType = QtWidgets.QLabel(dialog)
        self.label_msgType.setGeometry(QtCore.QRect(340, 100, 81, 21))
        self.label_msgType.setFont(font10)
        self.label_msgType.setObjectName("label_msgType")
        self.label_username = QtWidgets.QLabel(dialog)
        self.label_username.setGeometry(QtCore.QRect(30, 280, 81, 21))
        self.label_username.setFont(font10)
        self.label_username.setObjectName("label_username")
        self.input_box_msgType = QtWidgets.QComboBox(dialog)
        self.input_box_msgType.setGeometry(QtCore.QRect(430, 100, 191, 22))
        self.input_box_msgType.setFont(font10)
        self.input_box_msgType.setAutoFillBackground(True)
        self.input_box_msgType.setObjectName("input_box_msgType")
        self.input_box_msgType.addItem("")
        self.input_box_msgType.addItem("")
        self.groupBoxSendRequest = QtWidgets.QGroupBox(dialog)
        self.groupBoxSendRequest.setGeometry(QtCore.QRect(330, 20, 301, 301))
        self.groupBoxSendRequest.setFont(font9)
        self.groupBoxSendRequest.setObjectName("groupBoxSendRequest")
        self.button_displayAllCommands = QtWidgets.QPushButton(self.groupBoxSendRequest)
        self.button_displayAllCommands.setGeometry(QtCore.QRect(10, 220, 281, 28))
        self.button_displayAllCommands.setFont(font10)
        self.button_displayAllCommands.setObjectName("button_displayAllCommands")
        self.button_sendPackage = QtWidgets.QPushButton(self.groupBoxSendRequest)
        self.button_sendPackage.setGeometry(QtCore.QRect(10, 260, 281, 28))
        self.button_sendPackage.setFont(font10)
        self.button_sendPackage.setObjectName("button_sendPackage")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBoxSendRequest)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 110, 281, 101))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label_srcPort = QtWidgets.QLabel(dialog)
        self.label_srcPort.setGeometry(QtCore.QRect(30, 100, 69, 21))
        self.label_srcPort.setFont(font10)
        self.label_srcPort.setObjectName("label_srcPort")
        self.button_connect = QtWidgets.QPushButton(dialog)
        self.button_connect.setGeometry(QtCore.QRect(30, 180, 281, 28))
        self.button_connect.setFont(font10)
        self.button_connect.setObjectName("button_connect")
        self.input_destIP = QtWidgets.QLineEdit(dialog)
        self.input_destIP.setGeometry(QtCore.QRect(120, 60, 191, 22))
        self.input_destIP.setFont(font10)
        self.input_destIP.setObjectName("input_destIP")
        self.input_command = QtWidgets.QLineEdit(dialog)
        self.input_command.setGeometry(QtCore.QRect(430, 60, 191, 22))
        self.input_command.setFont(font10)
        self.input_command.setObjectName("input_command")
        self.button_register = QtWidgets.QPushButton(dialog)
        self.button_register.setGeometry(QtCore.QRect(30, 400, 281, 28))
        self.button_register.setFont(font10)
        self.button_register.setObjectName("button_register")
        self.input_password = QtWidgets.QLineEdit(dialog)
        self.input_password.setGeometry(QtCore.QRect(120, 320, 191, 22))
        self.input_password.setFont(font10)
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password.setObjectName("input_password")
        self.groupBoxCommandPrompt = QtWidgets.QGroupBox(dialog)
        self.groupBoxCommandPrompt.setGeometry(QtCore.QRect(10, 460, 311, 291))
        self.groupBoxCommandPrompt.setFont(font9)
        self.groupBoxCommandPrompt.setObjectName("groupBoxCommandPrompt")
        self.console_commandPrompt = QtWidgets.QTextBrowser(self.groupBoxCommandPrompt)
        self.console_commandPrompt.setGeometry(QtCore.QRect(10, 30, 281, 211))
        self.console_commandPrompt.setObjectName("console_commandPrompt")
        self.button_clearCmd = QtWidgets.QPushButton(self.groupBoxCommandPrompt)
        self.button_clearCmd.setGeometry(QtCore.QRect(10, 250, 281, 28))
        self.button_clearCmd.setFont(font10)
        self.button_clearCmd.setObjectName("button_clearCmd")
        self.button_login = QtWidgets.QPushButton(dialog)
        self.button_login.setGeometry(QtCore.QRect(30, 360, 281, 28))
        self.button_login.setFont(font10)
        self.button_login.setObjectName("button_login")
        self.input_srcPort = QtWidgets.QLineEdit(dialog)
        self.input_srcPort.setGeometry(QtCore.QRect(120, 100, 191, 22))
        self.input_srcPort.setFont(font10)
        self.input_srcPort.setObjectName("input_srcPort")
        self.input_username = QtWidgets.QLineEdit(dialog)
        self.input_username.setGeometry(QtCore.QRect(120, 280, 191, 22))
        self.input_username.setFont(font10)
        self.input_username.setObjectName("input_username")
        self.input_box_msgType.raise_()

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        dialog.setTabOrder(self.input_destIP, self.input_srcPort)
        dialog.setTabOrder(self.input_srcPort, self.input_destPort)
        dialog.setTabOrder(self.input_destPort, self.button_connect)
        dialog.setTabOrder(self.button_connect, self.input_username)
        dialog.setTabOrder(self.input_username, self.input_password)
        dialog.setTabOrder(self.input_password, self.button_login)
        dialog.setTabOrder(self.button_login, self.button_register)
        dialog.setTabOrder(self.button_register, self.input_command)
        dialog.setTabOrder(self.input_command, self.input_box_msgType)
        dialog.setTabOrder(self.input_box_msgType, self.plainTextEdit)
        dialog.setTabOrder(self.plainTextEdit, self.button_displayAllCommands)
        dialog.setTabOrder(self.button_displayAllCommands, self.button_sendPackage)
        dialog.setTabOrder(self.button_sendPackage, self.console_commandPrompt)
        dialog.setTabOrder(self.console_commandPrompt, self.button_clearCmd)
        dialog.setTabOrder(self.button_clearCmd, self.console_response)
        dialog.setTabOrder(self.console_response, self.button_clearResponse)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "CoAP Client"))
        self.groupBoxServerConnection.setTitle(_translate("dialog", "1. Server Connection"))
        self.groupBoxResponse.setTitle(_translate("dialog", "Response"))
        self.console_response.setHtml(_translate("dialog",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n""<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:7.8pt;\"><br /></p></body></html>"))
        self.button_clearResponse.setText(_translate("dialog", "Clear"))
        self.groupBoxSignIn.setTitle(_translate("dialog", "2. Sign In"))
        self.label_command.setText(_translate("dialog", "Command:"))
        self.label_destPort.setText(_translate("dialog", "Dest. port:"))
        self.label_password.setText(_translate("dialog", "Password:"))
        self.label_destIP.setText(_translate("dialog", "Dest. IP:"))
        self.label_msgType.setText(_translate("dialog", "Msg. type:"))
        self.label_username.setText(_translate("dialog", "Username:"))
        self.input_box_msgType.setItemText(0, _translate("dialog", "Confirmable"))
        self.input_box_msgType.setItemText(1, _translate("dialog", "Non-confirmable"))
        self.groupBoxSendRequest.setTitle(_translate("dialog", "3. Send Request"))
        self.button_displayAllCommands.setText(_translate("dialog", "Display All Commands"))
        self.button_sendPackage.setText(_translate("dialog", "Send Package"))
        self.label_srcPort.setText(_translate("dialog", "Src. port:"))
        self.button_connect.setText(_translate("dialog", "Connect"))
        self.button_register.setText(_translate("dialog", "Register"))
        self.groupBoxCommandPrompt.setTitle(_translate("dialog", "Command Prompt"))
        self.console_commandPrompt.setHtml(_translate("dialog",
                                                      "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n""<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:7.8pt;\"><br /></p></body></html>"))
        self.button_clearCmd.setText(_translate("dialog", "Clear Console"))
        self.button_login.setText(_translate("dialog", "Set authentication"))

    def counter(self):
        if self.connectedToServer == False:
            self.button_sendPackage.setEnabled(False)
            self.button_login.setEnabled(False)
            self.button_register.setEnabled(False)
        else:

            if len(self.input_command.text()) == 0:
                self.button_sendPackage.setEnabled(False)

            else:
                self.button_sendPackage.setEnabled(True)

            if len(self.input_username.text()) == 0 or len(self.input_password.text()) == 0:
                self.button_login.setEnabled(False)
                self.button_register.setEnabled(False)
            else:
                self.button_login.setEnabled(True)
                self.button_register.setEnabled(True)
        if receiver.receivedData != None:
            self.ReceivePackage()
            receiver.receivedData = None

    def ConnectToServer(self):
        if self.connectedToServer == False:
            # check the DIP format
            failure = False
            if isValidIP(self.input_destIP.text()) == False:
                self.console_commandPrompt.append("Invalid format for DIP")
                failure = True
            if isValidPort(self.input_srcPort.text()) == False or isValidPort(self.input_destPort.text()) == False:
                self.console_commandPrompt.append("Violation of Reserved Port")
                failure = True
            if failure == False:
                self.connectedToServer = True
                self.console_commandPrompt.append("Connected to the server")
                receiver.create_socket(self.input_srcPort.text())
                self.button_connect.setEnabled(False)
            else:
                self.console_commandPrompt.append("Failed to connect to the server")
        else:
            self.console_commandPrompt.append("Already connected to a server!")

    def Register(self):  # Method code 0.22
        headerString = createHeader(self.input_username.text(), self.input_password.text(), "register", self)

        # Sending the packet to the server:
        bytesToSend = bytes(headerString, encoding="latin_1")
        receiver.s.sendto(bytesToSend, (str(self.input_destIP.text()), int(self.input_destPort.text())))

    def Login(self):
        self.userID = self.input_username.text()
        self.password = self.input_password.text()
        self.console_commandPrompt.append("Logged in!")

    def SendPackage(self):
        if checkValidFunction(self.input_command.text()) == True:
            headerString = createHeader(self.userID, self.password, self.input_command.text(), self)
            # Sending the packet to the server:
            bytesToSend = bytes(headerString, encoding="latin_1")
            receiver.s.sendto(bytesToSend, (str(self.input_destIP.text()), int(self.input_destPort.text())))
        else:
            self.console_commandPrompt.append("Invalid command!")

    def ReceivePackage(self):
        # payload este de tip json:
        content = str(receiver.payload['content'])
        error = str(receiver.payload['error'])
        command = str(receiver.payload['command'])

        if content == "[]":
            content = ""

        if len(error) > 0:
            self.console_commandPrompt.append("Message with errors received from server")
            self.console_response.append("Error: " + error)
        else:
            if command == 'register':
                self.console_commandPrompt.append('Registered a new account to the server')
            else:
                self.console_commandPrompt.append("Message received from server")

            before_text = ""
            if command == 'cd':
                before_text = "Entered folder."
            elif command == 'ls':
                before_text = "All files are:\n"
                content = content.replace(",", "\n")
                content = content.replace("[", "")
                content = content.replace("]", "")
                content = content.replace(" ", "")
                content = content.replace("'", "")
            elif command == 'pwd':
                content = "Root" + content.split('Root')[1]
                before_text = "Path: "
            elif command == 'msg':
                before_text = 'Message delivered.'
            elif command == 'readText':
                before_text = 'Display text from file:\n'
            elif command == 'run':
                before_text = 'Run an executable file.'
            elif command == 'newFile':
                before_text = 'Created a new file.'
            elif command == 'newDir':
                before_text = 'Created a new directory.'
            elif command == 'rm':
                before_text = 'Removed a file.'
            elif command == 'copy':
                before_text = 'Copied a file.'
            elif command == 'paste':
                before_text = 'Pasted a file.'
            elif command == 'write':
                before_text = 'Wrote text to a file.'
            elif command == 'append':
                before_text = 'Appended text to a file.'
            self.console_response.append(before_text + content)

        self.console_response.append("")

    def ClearCommandPrompt(self):
        self.console_commandPrompt.clear()

    def ClearResponse(self):
        self.console_response.clear()

    def DisplayAllCommands(self):
        self.console_response.append("All the possible commands are:")
        for i in range(0, len(commandList)):
            self.console_response.append("- " + commandList[i] + "\t" + commandInfo[i])
        self.console_response.append("\n")

def checkValidFunction(request_type):
    if request_type.count('-') >= 1:
        command = request_type.split("-", 1)[0]
    elif request_type.count(' ') >= 1:
        command = request_type.split(" ", 1)[0]
    else:
        command = request_type
    command.replace(" ", "")

    if command in commandList:
        return True
    else:
        return False
