import sys
import threading
import serial
#import RPi.GPIO as GPIO
from time import sleep
import guiController
from data import DataManager
import message
from controller import Controller

ser = serial.Serial ("/dev/ttyS0", 115200)
threadLock = threading.Lock()
#table = {}
def getInput():
    while True:
        inp = input("")
        if(inp == "exit"):
            sys.exit()
        print("sending -> " + inp)
        guiController.updateSentCommandsListBox(inp)
        #sendRREQ(1, 1, 1, 1, 1, 1)
        sendData(inp)

def sendData(data):
    str(data)
    data += "\r\n"
    ser.write(data.encode())
    sleep(1)

def recieveData():
   # sender=""
    while True:
        if ser.in_waiting > 0:
            received_data = ser.read()
            sleep(0.3)
            data_left = ser.inWaiting()
            received_data += ser.read(data_left)
            receivedList = received_data.decode().split("\r\n")
            for x in receivedList:
                if x != "":
                    thread = DataManager(x, threadLock, ser)
                    thread.start()
            #print(receivedList)
            #receivedCommandWords = receivedList[0].split(",")
            #print(receivedCommandWords)
            #if len(receivedCommandWords) == 4:
             #   if receivedCommandWords[0] == "LR":
              #      sender = receivedCommandWords[1]
               #     sendData("AT+RSSI?")

                #elif receivedCommandWords[0] == "AT":
                 #   table[sender] = receivedCommandWords[1]
                  #  message = "hi " + sender + " " + "quality is" + receivedCommandWords[1]
                   # sendData("AT+SEND=" + len(message))
                   # sendData(message)
                   # print(table)
            #print("\nreceived: " + received_data.decode())
            guiController.updateReceivedCommandsListBox((received_data.decode())[:-2])



########### main thread #################
    print("resetting lora modul...")
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(18, GPIO.OUT)
    #GPIO.output(18, GPIO.HIGH)
    #sleep(1)
    #GPIO.output(18, GPIO.LOW)
    #GPIO.cleanup()
    guiController.serObj.ser = ser
    message.Message.ser = ser
    Controller.ser = ser


    guiController.guiInit()
    listener = threading.Thread(target=getInput)
    listener.start()
    reciever = threading.Thread(target=recieveData)
    reciever.start()
    guiController.guiDisplay()

############################################################################################
############################################################################################
    # ser.write("AT+CFG=433000000,20,9,12,4,1,0,0,0,0,3000,8,4\r\n".encode())
    # ser.write("AT+RX\r\n".encode())
    # ser.write("AT+ADDR=0003\r\n".encode())
    # sendData("AT+CFG=433000000,20,9,12,4,1,0,0,0,0,3000,8,4")
    # sendData("AT+RX")
    # sendData("AT+ADDR=0003")

#AT+CFG=433000000,20,9,10,4,1,0,0,0,0,3000,8,10
    #while True:
        #print("sending..")
        #ser.write("AT+SEND=5\r\n".encode())
        #sleep(0.5)
        #ser.write("Hallo\r\n".encode())
        #sleep(0.5)
        #received_data = ser.read()
        #sleep(0.3)
        #data_left = ser.inWaiting()
        #received_data += ser.read(data_left)
        #print("received: " + str(received_data))

     #   if ser.in_waiting > 0:
      #      received_data = ser.read()
       #     sleep(0.3)
        #    data_left = ser.inWaiting()
         #   received_data += ser.read(data_left)
          #  print("\nreceived: " + str(received_data))
