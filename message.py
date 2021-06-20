import serial
import time

class Message():
    ser = serial


    def sendRREQ(uFlag, hopCount, originAddr, originSeq, destAddr, destSeq):
        list = [1, uFlag, hopCount, originAddr, originSeq, destAddr, destSeq]
        array = bytearray(list)
        print(array)
        Message.sendData("AT+SEND=" + str(len(array)))
        Message.sendData(array.decode('ascii'))

    def sendRREP(hopCount, originAddr, destAddr, destSeq, lifetime):
        list = [2, hopCount, originAddr, destAddr, destSeq, lifetime]
        array = bytearray(list)
        print(array)
        Message.sendData("AT+SEND=" + str(len(array)))
        Message.sendData(array.decode('ascii'))

    def sendRERR(destCnt, destAddr, destSeq, additionalAddr, additionalSeq):
        list = [3, destCnt, destAddr, destSeq, additionalAddr, additionalSeq]
        array = bytearray(list)
        print(array)
        Message.sendData("AT+SEND=" + str(len(array)))
        Message.sendData(array.decode('ascii'))

    def sendRREPACK():
        list = [4]
        array = bytearray(list)
        print(array)
        Message.sendData("AT+SEND=" + str(len(array)))
        Message.sendData(array.decode('ascii'))

    def sendTextRequest(originAddr, destAddr, seqNr, payload):
        list = [5, hopCnt, originAddr, destAddr, seqNr, payload]
        array = bytearray(list)
        print(array)
        Message.sendData("AT+SEND=" + str(len(array)))
        Message.sendData(array.decode('ascii'))

    def sendTextHopACK(seqNr):
        list = [6, seqNr]
        array = bytearray(list)
        print(array)
        Message.sendData("AT+SEND=" + str(len(array)))
        Message.sendData(array.decode('ascii'))

    def sendTextRequestACK(originAddr, destAddr, seqNr):
        list = [7, originAddr, destAddr, seqNr]
        array = bytearray(list)
        print(array)
        Message.sendData("AT+SEND=" + str(len(array)))
        Message.sendData(array.decode('ascii'))

    def sendData(data):
        str(data)
        data += "\r\n"
        Message.ser.write(data.encode())
        time.sleep(1)