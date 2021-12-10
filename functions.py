
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

def isValidIP(ip):
    validFormat = True
    if ip.count('.') != 3:
        validFormat = False
    if validFormat == True:
        validFormat = ip.split('.')
        for i in range(4):
            if int(validFormat[i]) < 0 or int(validFormat[i]) > 255:
                validFormat = False
    return validFormat

def isValidPort(port):
    if port < 1024 or port > 65353:
        return False
    return True