import socket
import sys
import select
import threading
import json
import datetime
import random

def decimalToBinaryString(number,nbits):
    straux = str(bin(number))[2:]
    return (nbits - len(straux)) * "0" + straux

def increment16bits(s):
    if s == pow(2,16) -1:
        s = 0
    else:
        s = s + 1
    return s

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
if len(sys.argv) != 4:
    print("help : ")
    print("  --sport=numarul_meu_de_port ")
    print("  --dport=numarul_de_port_al_peer-ului ")
    print("  --dip=ip-ul_peer-ului ")
    sys.exit()

for arg in sys.argv:
    if arg.startswith("--sport"):
        temp, sport = arg.split("=")
    elif arg.startswith("--dport"):
        temp, dport = arg.split("=")
    elif arg.startswith("--dip"):
        temp, dip = arg.split("=")

# Creare socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

s.bind(('0.0.0.0', int(sport)))

running = True
messageID = 0

try:
    receive_thread = threading.Thread(target=receive_fct)
    receive_thread.start()
except:
    print("Eroare la pornirea thread‐ului")
    sys.exit()

while True:
    try:
        #-----------------------CREATE-HEADER---------------------------
        #---------------first-byte---------------
        # VER: 01
        octet1 = "01"

        # Type: CON (00), NON (01), ACK (10), RES (11)
        Type = "CON"
        if(Type == "CON"):
            octet1 += "00"
        elif(Type == "NON"):
            octet1 += "01"

        # Token Length
        tokenLength = 4  # must be between (0-8) #HIGH SECURITY - 8,  LOW SECURITY - 2
        octet1 += decimalToBinaryString(tokenLength,4)

        print("octet1: ", end='')
        print(bytes(octet1,encoding = "ascii"))

        # --------------second-byte----------------
        # Request Code
        octet2 = "00000001"

        #---------------message-id-----------------
        messageID = increment16bits(messageID)
        messageID_octeti = decimalToBinaryString(messageID, 16)
        print("Message ID: " + messageID_octeti)

        #---------------token----------------------
        token = []
        #este impartit si definit pe octeti
        for i in range (tokenLength):
            token_octet = ""
            for j in range(8):
                token_octet += str(random.choice([0,1]))
            token.append(token_octet)
        print(token)

        #---------------payload--------------------
        username = "Tudisie"
        passwd = "matapegheata"

        request_type = input("Request Type: ")
        command, parameters = request_type.split("-", 1)
        command.replace(" ", "")
        parameters.replace(" ","")
        parameters = "-" + parameters

        request = {
            "username": username,
            "password": passwd,
            "command": command,
            #command: ls, dir
            "parameters": parameters,
            #parameters: -l, -r
            "timestamp": str(datetime.datetime.now())
        }

        #converting into JSON:
        request_json = json.dumps(request)

        #sending the JSON:
        s.sendto(bytes(request_json, encoding="ascii"), (dip, int(dport)))
    except KeyboardInterrupt:
        running = False
        print("Waiting for the thread to close...")
        receive_thread.join()
        break
