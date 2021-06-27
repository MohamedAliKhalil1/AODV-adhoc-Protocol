import threading

import data
from message import Message
from datetime import datetime
import serial
import time
import json

def checkNieghbours():
    table = data.DataManager.table
    destChekNum = {}
    while True:
        for dest in table:
            if destChekNum.__contains__(dest) == False:
                destChekNum[dest] = 1
            else:
                destChekNum[dest] = destChekNum[dest] + 1
            if datetime.now().timestamp() > table[dest][2]: #turn the route to unvalid
                table[dest][4] = False;
                Controller.send("AT+DEST=FFFF")
                Controller.seqNr = (Controller.seqNr + 1) % 256
                table[dest][1] = (table[dest][1]+1)%256
                Message.sendRREQ(0, 0, 1, Controller.myAddr, Controller.seqNr, Controller.destAddr, table[dest][1])
            else:
                destChekNum[dest] = 0
            if(destChekNum[dest] > 3 and table[dest][4] == False): #RRER -> Typ, destCnt, destAddr, destSeq, additionalAddr, additionalSeq
                Controller.send("AT+DEST=FFFF")
                Controller.seqNr = (Controller.seqNr + 1) % 256
                Message.sendRERR(1, dest, table[dest][1], dest, table[dest[1]])
                for d in table:
                    if table[d][3] == dest:
                        table.pop(d)

        time.sleep(7)


class Controller():
    threadLock = threading.Lock()
    ser = serial
    myAddr = 0
    destAddr = 0
    sendMode = False
    seqNr = 0
    prevHop = 0
    waitingForRREPlist = list()
    lifeTime = 180
    tosend = ""
    toSendMap = {}
    id = 1
    payloadLength = 0
    bearbeitet = {}

    def send(data):
        str(data)
        data += "\r\n"
        Controller.ser.write(data.encode())
        time.sleep(1)

    def parseInput(self, inp):
        if (inp == "table"):
            print("I know now: " + json.dumps(data.DataManager.table)) # [dest -> [hopCnt, destSeq, lifeTime, nextHop , valid] ]
        else:
            inpList = inp.split("=")
            if (inpList[0] == "AT+SEND"):
                Controller.sendMode = True
                Controller.payloadLength = int(inpList[1])
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
                    Controller.seqNr = (Controller.seqNr + 1)%256
                    Message.sendRREQ(0, 0, 1, Controller.myAddr, Controller.seqNr, Controller.destAddr, 0)
                else:
                    Controller.send("AT+DEST=" + str(Controller.destAddr))
            elif (Controller.sendMode):
                if (data.DataManager.table.__contains__(Controller.destAddr)):
                    # send uni cast to the next hop of the dest
                    Controller.send("AT+DEST=" + str(data.DataManager.table[Controller.destAddr][3]))
                    Controller.seqNr = (Controller.seqNr + 1)%256
                    Message.sendTextRequest(Controller.myAddr, Controller.destAddr, Controller.seqNr, Controller.seqNr, inpList[0])
                    Controller.sendMode = False
                    Controller.tosend = ""
                else:
                    Controller.send("AT+DEST=FFFF")
                    Controller.seqNr = (Controller.seqNr + 1)%256
                    Message.sendRREQ(0, 0, 1, Controller.myAddr, Controller.seqNr, Controller.destAddr, 0)
                    Controller.tosend = inpList[0]
                    Controller.toSendMap[Controller.destAddr] = inpList[0] # add send pending message buffer
            else:
                Controller.send(inp)

    def parseRecieved(self, response):
       # time.sleep(0.5)
       # Controller.threadLock.acquire()
        receivedCommandWords = self.response.split(",")
        print("Controller: " + str(receivedCommandWords))

        if len(receivedCommandWords) == 4:
            if receivedCommandWords[0] == "LR":
                Controller.prevHop = int(receivedCommandWords[1])
                print(ord(receivedCommandWords[3][0]))
                if (ord(receivedCommandWords[3][0]) == 1):  # RREQ {type, uFlag, id, hopCount, originAddr, originSeq, destAddr, destSeq}

                    uFlag = ord(receivedCommandWords[3][1])
                    hopCnt = ord(receivedCommandWords[3][2])
                    id = ord(receivedCommandWords[3][3])
                    originAddr = ord(receivedCommandWords[3][4])
                    originSeq = ord(receivedCommandWords[3][5])
                    destAddr = ord(receivedCommandWords[3][6])
                    destSeq = ord(receivedCommandWords[3][7])

                    print("RREQ Empfangen " + " prevHOP: " + str(Controller.prevHop) + " OriginAddr: " + str(
                        originAddr) + " destAddr: " + str(destAddr))

                    if (destAddr == Controller.myAddr):  # i am the distination, then send rrep to prevHop
                        Controller.send("AT+DEST=" + str(Controller.prevHop))
                        hopCnt += 1
                        Controller.seqNr = (Controller.seqNr + 1) % 256
                        Message.sendRREP(hopCnt, originAddr, Controller.myAddr, Controller.seqNr, Controller.lifeTime)
                    elif originAddr != Controller.myAddr and Controller.bearbeitet.__contains__((Controller.prevHop,destAddr, destSeq)) == False: # drop th rreq if i am the originator

                        if (destAddr == Controller.myAddr):  # i am the distination, then send rrep to prevHop
                            Controller.send("AT+DEST=" + str(Controller.prevHop))
                            hopCnt += 1
                            Controller.seqNr = (Controller.seqNr + 1)%256
                            Message.sendRREP(hopCnt, originAddr, Controller.myAddr, Controller.seqNr,Controller.lifeTime)

                        elif data.DataManager.table.__contains__(destAddr):
                            # i have route to target then send unicast to the prevHop
                            Controller.send("AT+DEST=" + str(Controller.prevHop))
                            Message.sendRREP(data.DataManager.table[destAddr][0], originAddr, destAddr,
                                             data.DataManager.table[destAddr][1], data.DataManager.table[destAddr][2])
                            Controller.bearbeitet[(Controller.prevHop, destAddr, destSeq)] = True
                        else:
                            data.DataManager.pendingRREP[(originAddr, destAddr)] = Controller.prevHop
                            Controller.send("AT+DEST=FFFF")
                            hopCnt += 1
                            Message.sendRREQ(0, hopCnt, '1', originAddr, originSeq, destAddr, destSeq)
                            Controller.bearbeitet[(Controller.prevHop, destAddr, destSeq)] = True

                elif (ord(receivedCommandWords[3][0]) == 2):  # RREP [type, hopCount, originAddr, destAddr, destSeq, lifetime]
                    hopCnt = ord(receivedCommandWords[3][1])
                    originAddr = ord(receivedCommandWords[3][2])
                    destAddr = ord(receivedCommandWords[3][3])
                    destSeq = ord(receivedCommandWords[3][4])
                    lifeTime = ord(receivedCommandWords[3][5])

                    # hier ack must be sended to the prevHop
                    Controller.send("AT+DEST=" + str(Controller.prevHop))
                    Message.sendRREPACK()

                    if (data.DataManager.table.__contains__(destAddr) and Controller.isValidRoute(destAddr)):  # update
                        # [dest -> [hopCnt, destSeq, lifeTime, nextHop , valid] ]
                        table = data.DataManager.table
                        table[destAddr] = [
                            hopCnt,
                            max(table[destAddr][1], destSeq),
                            lifeTime + datetime.now().timestamp(),
                            Controller.prevHop,
                            True
                        ]
                    else:
                        table = data.DataManager.table
                        table[destAddr] = [
                            hopCnt,
                            destSeq,
                            lifeTime + datetime.now().timestamp(),
                            Controller.prevHop,
                            True
                        ]

                    if (Controller.myAddr != originAddr):  # muss weiter geleitet?
                        if (data.DataManager.pendingRREP.__contains__((originAddr, destAddr))):
                            Controller.send("AT+DEST=" + str(data.DataManager.pendingRREP(originAddr, destAddr)))
                            Message.sendRREP(++hopCnt, originAddr, destAddr, destSeq, lifeTime)
                            data.DataManager.pendingRREP.pop((originAddr, destAddr))




                elif (ord(receivedCommandWords[3][0]) == 5):
                    originAddr = ord(receivedCommandWords[3][1])
                    destAddr = ord(receivedCommandWords[3][2])
                    seqNr = ord(receivedCommandWords[3][3])
                    # payload = receivedCommandWords[3][4]
                    messageLen = len(receivedCommandWords[3]) - 4
                    # print(messageLen)
                    payload = receivedCommandWords[3][4]
                    for x in range(5, 4 + messageLen):
                        payload += receivedCommandWords[3][x]
                    print(payload)
                    # print(receivedCommandWords[3][5])

                    Controller.send("AT+DEST=" + str(Controller.prevHop))
                    Message.sendTextHopACK(seqNr)

                    print("recieved from " + str(Controller.prevHop) + "destination is " + str(
                        destAddr) + "-> " + str(payload))

                    if (destAddr == Controller.myAddr):
                        Controller.send("AT+DEST=" + str(Controller.prevHop))
                        Message.sendTextRequestACK(originAddr, destAddr, seqNr)
                        print("recieved from " + str(Controller.prevHop) + "destination is me " + str(
                            destAddr) + "-> " + str(payload))
                    else:  # muss weitergeleitet werden
                        if (data.DataManager.table.__contains__(destAddr)):
                            # send to the next hop
                            Controller.send("AT+DEST=" + str(data.DataManager.table[destAddr][3]))
                            Message.sendTextRequest(originAddr, destAddr, seqNr, payload)
     #   Controller.threadLock.release()
      #  time.sleep(0.5)

        # x = Message()
        #  x.sendRREQ(1, 1, 1, 1, 1, 1)
        #   Controller.send("AT+RSSI?")
        # elif receivedCommandWords[0] == "AT":
        # table[DataManager.sender] = receivedCommandWords[1]
        # message = "hi " + DataManager.sender + " " + "quality is " + receivedCommandWords[1]
        # Controller.send("AT+SEND=" + str(len(message)))
        # Controller.send(message)
        # message = "I know now: " + json.dumps(data.DataManager.table)
        # time.sleep(2)
        # Controller.send("AT+SEND=" + str(len(message)))
        # print(DataManager.table)


    def isValidRoute(dest):
        table = data.DataManager.table  # [dest -> [hopCnt, destSeq, lifeTime, nextHop , valid] ]
        return table[dest][4] == True