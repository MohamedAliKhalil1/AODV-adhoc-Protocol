
import serial
import time

class Message():
    ser = serial

    def sendRREQ(uFlag, hopCount, id, originAddr, originSeq, destAddr, destSeq):
        # list = [1, uFlag, hopCount,id, originAddr, originSeq, destAddr, destSeq]
        # array = bytearray(list)
        # print(array)

        message = b"".join([Message.convert_to_bytes(1),
                            Message.convert_to_bytes(uFlag),
                            Message.convert_to_bytes(hopCount),
                            Message.convert_to_bytes(id),
                            Message.convert_to_bytes(originAddr),
                            Message.convert_to_bytes(originSeq),
                            Message.convert_to_bytes(destAddr),
                            Message.convert_to_bytes(destSeq)
                            ])

        print("type " + str(Message.convert_to_bytes(1)))
        print("u-flag " + str(Message.convert_to_bytes(uFlag)))
        print("hops" + str(Message.convert_to_bytes(hopCount)))
        print("id " + str(Message.convert_to_bytes(id)))
        print("originAddr " + str(Message.convert_to_bytes(originAddr)))
        print("priginSEQ " + str(Message.convert_to_bytes(originSeq)))
        print("destAddr " + str(Message.convert_to_bytes(destAddr)))
        print("destSEQ " + str(Message.convert_to_bytes(destSeq)))

        Message.sendData(("AT+SEND=" + str(len(message)) + "\r\n").encode())
        Message.sendData(message)

    def sendRREP(hopCount, originAddr, destAddr, destSeq, lifetime):
        # list = [2, hopCount, originAddr, destAddr, destSeq, lifetime]
        # array = bytearray(list)
        #  print(array)
        # Message.sendData(f"AT+SEND={len(array)}")
        #  Message.sendData(array.decode())

        message = b"".join([Message.convert_to_bytes(2),
                            Message.convert_to_bytes(hopCount),
                            Message.convert_to_bytes(originAddr),
                            Message.convert_to_bytes(destAddr),
                            Message.convert_to_bytes(destSeq),
                            Message.convert_to_bytes(lifetime),
                            b"\r\n"])

        Message.sendData(("AT+SEND=" + str(len(message)) + "\r\n").encode())
        Message.sendData(message)

    def sendRERR(destCnt, destAddr, destSeq, additionalAddr, additionalSeq):
        # list = [3, destCnt, destAddr, destSeq, additionalAddr, additionalSeq]
        #  array = bytearray(list)
        # print(array)
        #  Message.sendData("AT+SEND=" + str(len(array)))
        # Message.sendData(array.decode())

        message = b"".join([Message.convert_to_bytes(3),
                            Message.convert_to_bytes(destCnt),
                            Message.convert_to_bytes(destAddr),
                            Message.convert_to_bytes(destSeq),
                            Message.convert_to_bytes(additionalAddr),
                            Message.convert_to_bytes(additionalSeq),
                            b"\r\n"])

        Message.sendData(("AT+SEND=" + str(len(message)) + "\r\n").encode())
        Message.sendData(message)

    def sendRREPACK():
        #    list = [4]
        #   array = bytearray(list)
        #  print(array)
        # Message.sendData("AT+SEND=" + str(len(array)))
        # Message.sendData(array.decode())

        message = b"".join([Message.convert_to_bytes(4),
                            b"\r\n"])

        Message.sendData(("AT+SEND=" + str(len(message)) + "\r\n").encode())
        Message.sendData(message)

    def sendTextRequest(self, originAddr, destAddr, seqNr, payload):
        #  list = [5, hopCnt, originAddr, destAddr, seqNr, payload]
        #   array = bytearray(list)
        #  print(array)
        #  Message.sendData("AT+SEND=" + str(len(array)))
        #  Message.sendData(array.decode())

        print("originAddr " + str(Message.convert_to_bytes(originAddr)))
        print("priginSEQ " + str(Message.convert_to_bytes(originAddr)))
        print("destAddr " + str(Message.convert_to_bytes(destAddr)))
        print("destSEQ " + str(Message.convert_to_bytes(seqNr)))
        print("payload " + str(Message.convert_to_bytes(payload)))

        message = b"".join([Message.convert_to_bytes(5),
                            Message.convert_to_bytes(originAddr),
                            Message.convert_to_bytes(destAddr),
                            Message.convert_to_bytes(seqNr),
                            Message.convert_to_bytes(payload),
                            b"\r\n"])

        Message.sendData(("AT+SEND=" + str(len(message)) + "\r\n").encode())
        Message.sendData(message)

    def sendTextHopACK(seqNr):
        #     list = [6, seqNr]
        #    array = bytearray(list)
        #   print(array)
        #  Message.sendData("AT+SEND=" + str(len(array)))
        # Message.sendData(array.decode())

        message = b"".join([Message.convert_to_bytes(6),
                            Message.convert_to_bytes(seqNr),
                            b"\r\n"])

        Message.sendData(("AT+SEND=" + str(len(message)) + "\r\n").encode())
        Message.sendData(message)

    def sendTextRequestACK(originAddr, destAddr, seqNr):
        #    list = [7, originAddr, destAddr, seqNr]
        #   array = bytearray(list)
        #  print(array)
        # Message.sendData("AT+SEND=" + str(len(array)))
        # Message.sendData(array.decode())

        message = b"".join([Message.convert_to_bytes(7),
                            Message.convert_to_bytes(originAddr),
                            Message.convert_to_bytes(destAddr),
                            Message.convert_to_bytes(seqNr),
                            b"\r\n"])

        Message.sendData(("AT+SEND=" + str(len(message)) + "\r\n").encode())
        Message.sendData(message)

    def convert_to_bytes(inp):
        if isinstance(inp, str):
            return inp.encode()
        elif isinstance(inp, int):
            return bytes([inp])

    def sendData(data):
        str(data)
        print("sending message -> " + str(data))
        Message.ser.write(data)
        time.sleep(1)



