import data
from message import Message
import serial
import time
import json

class Controller():
    ser = serial
    myAddr = 0
    destAddr = 0
    sendMode = False
    seqNr = 0
    sender = 0
    waitingForRREPlist = list()
    lifeTime = 5
    tosend = ""

    def send(data):
        str(data)
        data += "\r\n"
        Controller.ser.write(data.encode())
        time.sleep(1)

    def parseInput(self, inp):
        if(inp == "table"):
            print("I know now: " + json.dumps(data.DataManager.table))
        else:
            inpList = inp.split("=")
            if (inpList[0] == "AT+SEND"):
                Controller.sendMode = True
            elif (inpList[0] == "AT+ADDR"):
                Controller.sendMode = False
                Controller.myAddr = int(inpList[1])
                Controller.send(inp)
            elif (inpList[0] == "AT+DEST"):
                Controller.sendMode = False
                Controller.destAddr = int(inpList[1])
                if (data.DataManager.table.__contains__(Controller.destAddr) == False):  # not route found -> send RREQ
                    Controller.waitingForRREPlist.append(Controller.destAddr)
                    Controller.send("AT+DEST=FFFF")
                    Message.sendRREQ(0, 0, Controller.myAddr, ++(Controller.seqNr), Controller.destAddr, 0)
                else:
                    Controller.send("AT+DEST=" + str(Controller.destAddr))
            elif (Controller.sendMode):
                if (data.DataManager.table.__contains__(Controller.destAddr)):
                    Controller.send("AT+DEST=" + str(Controller.destAddr))
                    Message.sendTextRequest(data.DataManager.table[Controller.destAddr][0],
                                            Controller.myAddr, Controller.destAddr, ++(Controller.seqNr), inpList[0])
                    Controller.sendMode = False
                    Controller.tosend = ""
                else:
                    Controller.send("AT+DEST=FFFF")
                    Message.sendRREQ(0, 0, Controller.myAddr, ++(Controller.seqNr), Controller.destAddr, 0)
                    Controller.tosend = inpList[0]
            else:
                Controller.send(inp)

    def parseRecieved(self, response):
        receivedCommandWords = self.response.split(",")
        print("Controller: " + str(receivedCommandWords))

        if len(receivedCommandWords) == 4:
            if receivedCommandWords[0] == "LR":
                Controller.sender = ord(receivedCommandWords[1])
                if (ord(receivedCommandWords[3][
                            0]) == 1):  # RREQ {type, uFlag, hopCount, originAddr, originSeq, destAddr, destSeq}
                    originAddr = ord(receivedCommandWords[3][3])
                    hopCnt = ord(receivedCommandWords[3][2])
                    originSeq = ord(receivedCommandWords[3][4])
                    senderAddr = ord(receivedCommandWords[1])
                    destAddr = ord(receivedCommandWords[3][5])
                    destSeq = ord(receivedCommandWords[3][6])
                    if (originAddr != Controller.myAddr):
                        if (destAddr == Controller.myAddr):  # i am the distination
                            Controller.send("AT+DEST=" + str(senderAddr))
                            Message.sendRREP(++hopCnt, originAddr, Controller.myAddr, ++(Controller.seqNr),
                                             Controller.lifeTime)
                        elif (data.DataManager.table.__contains__(destAddr)):  # send unicast to the sender
                            # send RREP to the sender
                            Controller.send("AT+DEST=" + str(senderAddr))
                            Message.sendRREP(data.DataManager.table[destAddr][0], originAddr, Controller.myAddr,
                                             data.DataManager.table[destAddr][1], Controller.lifeTime)
                        else:
                            data.DataManager.pendingRREP[(originAddr, destAddr)] = True
                            Controller.send("AT+DEST=FFFF")
                            Message.sendRREQ(0, ++hopCnt, originAddr, originSeq, destAddr, destSeq)

                elif (ord(receivedCommandWords[3][
                              0]) == 2):  # RREP [type, hopCount, originAddr, destAddr, destSeq, lifetime]
                    hopCnt = ord(receivedCommandWords[3][1])
                    originAddr = ord(receivedCommandWords[3][2])
                    destAddr = ord(receivedCommandWords[3][3])
                    destSeq = ord(receivedCommandWords[3][4])
                    lifeTime = ord(receivedCommandWords[3][5])
                    sender = ord(receivedCommandWords[1])

                    # hier ack must be sended to the sender
                    Controller.send("AT+DEST=" + str(sender))
                    Message.sendRREPACK()

                    data.DataManager.table[destAddr] = [hopCnt, destSeq, lifeTime, sender]

                    if (Controller.myAddr != originAddr):  # muss weiter geleitet?
                        if (data.DataManager.pendingRREP.__contains__((originAddr, destAddr))):
                            Controller.send("AT+DEST=" + str(originAddr))
                            Message.sendRREP(++hopCnt, originAddr, destAddr, destSeq, lifeTime)

                elif (ord(receivedCommandWords[3][0]) == 5):
                    originAddr = ord(receivedCommandWords[3][1])
                    destAddr = ord(receivedCommandWords[3][2])
                    seqNr = ord(receivedCommandWords[3][3])
                    payload = ord(receivedCommandWords[3][4])

                    Controller.send("AT+DEST=" + str(Controller.sender))
                    Message.sendTextHopACK(seqNr)

                    print("recieved from " + str(Controller.sender) + "destination is " + str(
                        destAddr) + "-> " + payload)

                    if (destAddr == Controller.myAddr):
                        Controller.send("AT+DEST=" + str(Controller.sender))
                        Message.sendTextRequestACK(originAddr, destAddr, seqNr)
                        print("recieved from " + str(Controller.sender) + "destination is me " + str(
                            destAddr) + "-> " + payload)
                    else:  # muss weitergeleitet werden
                        if (data.DataManager.table.__contains__(destAddr)):
                            # send to the next hop
                            Controller.send("AT+DEST=" + str(data.DataManager.table[destAddr][3]))
                            Message.sendTextRequest(originAddr, destAddr, seqNr, payload)

        # x = Message()
          #  x.sendRREQ(1, 1, 1, 1, 1, 1)
         #   Controller.send("AT+RSSI?")
        #elif receivedCommandWords[0] == "AT":
            #table[DataManager.sender] = receivedCommandWords[1]
            #message = "hi " + DataManager.sender + " " + "quality is " + receivedCommandWords[1]
            #Controller.send("AT+SEND=" + str(len(message)))
            #Controller.send(message)
            #message = "I know now: " + json.dumps(data.DataManager.table)
            #time.sleep(2)
            #Controller.send("AT+SEND=" + str(len(message)))
           # print(DataManager.table)


