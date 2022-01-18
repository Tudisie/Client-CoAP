import select
import socket
import sys, threading
from functions import string2bits, getBytesListFromString, bits2string
import json

running = False
s = None
receivedData = None

receivedAcknowledge = False
receivedCON = False

global version, type, tokenLength, clss, code, msgID, token, payload


def checkMessage(list):
    global version, type, tokenLength, clss, code, msgID, token, payload, receivedAcknowledge, receivedCON
    octet1 = list[0]
    version = octet1[0:2]
    type = octet1[2:4]
    tokenLength = octet1[4:8]

    print("------------################## TIPUL MESAJULUI PRIMIT = " + str(type) + " ####################--------------------")
    if type == "10":
        receivedAcknowledge = True
        receivedCON = False
    elif type == "00":
        receivedAcknowledge = False
        receivedCON = True
    else:
        receivedAcknowledge = False
        receivedCON = False

    if version != "01":
        print("Eroare: Wrong version of CoAP!")
    if int(tokenLength[0]) & (int(tokenLength[1]) | int(tokenLength[2]) | int(tokenLength[3])):
        print("Eroare: Token Length exceeds the maximum value")

    octet2 = list[1]
    clss = int(octet2[0:3],2)
    code = int(octet2[3:8],2)

    msgID = int(list[2],2)

    token = list[3]
    payloadString = ""
    for i in range(5,len(list)):
        payloadString += chr(int(list[i], 2))
    payload = json.loads(payloadString)

    print(payloadString)

def receive_fct():
    global running, s, receivedData
    contor = 0
    while running:
        # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
        # Stabilim un timeout de 1 secunda
        if s != None:
            r, _, _ = select.select([s], [], [], 1)
            if not r:
                contor = contor + 1
            else:
                receivedData, address = s.recvfrom(4096)
                receivedDataString = receivedData.decode('latin_1')

                #lista primita de la server este un string integral, deci trebuie sa o facem lista si sa eliminam caracterele suplimentare
                print(receivedDataString)
                list = receivedDataString.split(',')
                checkMessage(getBytesListFromString(list))

#Receive Thread
def threadInit():
    try:
        receive_thread = threading.Thread(target=receive_fct)
        receive_thread.start()
    except:
        print("Eroare la pornirea thread‐ului")
        sys.exit()

# Creare socket UDP
def create_socket(sport):
    global running, s

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind(('0.0.0.0', int(sport)))
    running = True
    threadInit()