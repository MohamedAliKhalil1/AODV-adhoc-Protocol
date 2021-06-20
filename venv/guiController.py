import tryGUI
from datetime import datetime
import serial
from time import sleep
from controller import Controller

class serObj:
    ser = serial

def guiInit():
    tryGUI.sendButton.update_command(sendButtonListner)

def sendButtonListner():
    Controller.parseInput(tryGUI.commandTextBox.value)
    #sendData(tryGUI.commandTextBox.value)
    updateSentCommandsListBox(tryGUI.commandTextBox.value)
    tryGUI.commandTextBox.clear()

def updateSentCommandsListBox(command):
    if(command != ""):
        tryGUI.sentCommandsListbox.append(command)

def updateReceivedCommandsListBox(command):
    display = "["+datetime.now().strftime("%H:%M:%S")+"] " + command
    tryGUI.receivedCommandsListBox.append(display)

def guiDisplay():
    tryGUI.app.display()

def sendData(data):
    str(data)
    data += "\r\n"
    serObj.ser.write(data.encode())
    sleep(0.5)

