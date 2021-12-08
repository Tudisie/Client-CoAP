import socket
import sys
import select
import threading
import json
import datetime
import random
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow, QPushButton, QVBoxLayout, QDesktopWidget
from PyQt5.QtCore import QTimer



# ------------------------- Global Variables ------------------------- #
messageID = 0

# ------------------------------------------------------------------------- #
# --------------------------- Helper-Functions ---------------------------- #
# ------------------------------------------------------------------------- #

def decimalToBinaryString(number,nbits):
    straux = str(bin(number))[2:]
    return (nbits - len(straux)) * "0" + straux

def increment16bits(s):
    if s == pow(2,16) -1:
        s = 0
    else:
        s = s + 1
    return s

def string2bits(s):
    return [bin(ord(x))[2:].zfill(8) for x in s]

def bits2string(b):
    return ''.join([chr(int(x, 2)) for x in b])


def header_FirstByte():
    # --------------- first-byte --------------- #
    # VER: 01
    octet1 = "01"

    # Type: CON (00), NON (01), ACK (10), RES (11)
    Type = "CON"
    if Type == "CON":
        octet1 += "00"
    elif Type == "NON":
        octet1 += "01"

    # Token Length
    tokenLength = 4  # must be between (0-8) #HIGH SECURITY - 8,  LOW SECURITY - 2
    octet1 += decimalToBinaryString(tokenLength, 4)

    return octet1

def header_SecondByte():
    # -------------- second-byte ---------------- #
    # Request/Response Code
    octet2 = "00000001"

    return octet2

def header_MessageID():
    # --------------- message-id ----------------- #
    global messageID
    messageID = increment16bits(messageID)
    messageID_string = decimalToBinaryString(messageID, 16)  # e pe 16 biti
    messageID_octet1 = messageID_string[0:7]
    messageID_octet2 = messageID_string[8:15]

    return [messageID_octet1, messageID_octet2]

def header_Token():
    # --------------- token ---------------------- #
    token = []
    octet1 = header_FirstByte()
    tokenLength = int(octet1[4] + octet1[5] + octet1[6] + octet1[7], 2)
    # este impartit pe octeti (este generat random -> rol in securitatea comunicatiei)
    for i in range(tokenLength):
        token_octet = ""
        for j in range(8):
            token_octet += str(random.choice([0, 1]))
        token.append(token_octet)

    return token


def header_SeparatingByte():
    # --------------- biti delimitare payload ----------------- #
    biti_delimitare = "11111111"

    return biti_delimitare

def header_Payload():
    # --------------- payload -------------------- #
    username = "Tudisie"
    passwd = "mypasswd"

    request_type = "ls -l"
    command, parameters = request_type.split("-", 1)
    command.replace(" ", "")
    parameters.replace(" ", "")
    parameters = "-" + parameters

    request = {
        "username": username,
        "password": passwd,
        "command": command,  # ls, dir
        "parameters": parameters,  # -l, -r
        "timestamp": str(datetime.datetime.now())
    }

    # converting to JSON:
    request_json = json.dumps(request)

    return string2bits(request_json)


# ------------------------------------------------------------------------- #
# --------------------------- Core functions ------------------------------ #
# ------------------------------------------------------------------------- #

def createHeader():
    # creating the entire header
    header = []
    header.append(header_FirstByte())
    header.append(header_SecondByte())
    header.append(header_MessageID()[0])
    header.append(header_MessageID()[1])
    for o in header_Token():
        header.append(o)
    header.append(header_SeparatingByte())
    for o in header_Payload():
        header.append(o)

    # In acest moment avem header-ul complet (este o lista de stringuri, fiecare string reprezentand un sir de 8 "biti"
    # Vom transforma fiecare string intr-un caracter corespunzator
    header_string = bits2string(header)
    print(header_string)

    return header_string


# ------------------------------------------------------------------------- #
# ----------------------------- Main program ------------------------------ #
# ------------------------------------------------------------------------- #


def receive_fct():
    global running
    contor = 0
    while running:
        # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
        # Stabilim un timeout de 1 secunda
        r, _, _ = select.select([s], [], [], 1)
        if not r:
            contor = contor + 1
        else:
            data, address = s.recvfrom(1024)
            print("S-a receptionat ", str(data), " de la ", address)
            print("Contor = ", contor)


# Citire nr port din linia de comanda
print("help : ")
print("  --sport=numarul_meu_de_port ")
print("  --dport=numarul_de_port_al_peer-ului ")
print("  --dip=ip-ul_peer-ului ")

sport = "10001"
dport = "10010"
dip = "192.168.0.196"

# Creare socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.bind(('0.0.0.0', int(sport)))
running = True

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "CoAP Client"
        self.width = 480
        self.height = 800

        self.initUI()
        self.threadInit()

    #Receive Thread
    def threadInit(self):
        try:
            receive_thread = threading.Thread(target=receive_fct)
            receive_thread.start()
        except:
            print("Eroare la pornirea thread‐ului")
            sys.exit()

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

        self.button = QPushButton("Send Package",self)
        self.button.move(50, 200)
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_clicked_SendPackage)

        self.show()

    def button_clicked_SendPackage(self):
        self.timerButtonDisabled = 10
        headerString = createHeader()

        # Sending the packet to the server:
        s.sendto(bytes(headerString, encoding="utf-8"), (dip, int(dport)))

    def counter(self):
        if self.timerButtonDisabled:
            self.timerButtonDisabled -= 1
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)
windows = App()
sys.exit(app.exec_())