import json
import datetime
import random

from functions import *
import interface

def createHeader(username, passwd, request_type):
    # creating the entire header
    header = []
    header.append(header_FirstByte())
    header.append(header_SecondByte())
    msgID = header_MessageID()
    header.append(msgID[0])
    header.append(msgID[1])
    for o in header_Token():
        header.append(o)
    header.append(header_SeparatingByte())
    for o in header_Payload(username, passwd, request_type):
        header.append(o)

    # In acest moment avem header-ul complet (este o lista de stringuri, fiecare string reprezentand un sir de 8 "biti"
    # Vom transforma fiecare string intr-un caracter corespunzator
    header_string = bits2string(header)
    print(header_string)

    return header_string


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

messageID = 0

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

def header_Payload(username, passwd, request_type):
    # --------------- payload -------------------- #

    if request_type.count('-') >= 1:
        command, parameters = request_type.split("-", 1)
        parameters.replace(" ", "")
        parameters = "-" + parameters
    else:
        command = request_type
        parameters = "None"
    command.replace(" ", "")

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