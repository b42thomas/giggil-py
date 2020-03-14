import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import threading
import queue
import requests
from time import sleep # Import the sleep function from the time module

#pins
TICK_SENSOR_PIN = 11

#global vars
tickStatus = GPIO.LOW
tickCount = 0
previousTickCount = tickCount
scanBuffer = ""


class Item:
 scanString = "phantom"
 ID = -1
 pos = -1
 
 def __init__(self,scanStr):
  self.scanString = scanStr
 def setId(newId):
  ID = newId
 

def getInput(r, c, prompt_string):
    global textScreen
    curses.echo() 
    (r, c, prompt_string)
    textScreen.refresh()
    myInp = textScreen.getstr(r + 1, c, 20)
    return myInp  #

#items list
items = []

def getItem(scanString):
 global items
 for currentItem in items:
  if (currentItem.scanString == scanString):
   return currentItem
 return False

def setup():
 print("setting up beep boop")

 GPIO.setwarnings(False) # Ignore warning for now
 GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
 GPIO.setup(11, GPIO.OUT) # Set pin 8 to be an output pin and set initial value to low (off)
 GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
 counter = 0
 pwm=GPIO.PWM(11, 50)
 pwm.start(0)
 tickStatus = GPIO.LOW
 tickCount = 0
 
 
def checkConfigChanges():
 print("checking config changes boop boop")

def updateTickSensor():
 global tickStatus
 global tickCount
 if (GPIO.input(TICK_SENSOR_PIN) != tickStatus):
  tickStatus = GPIO.input(TICK_SENSOR_PIN)
  tickCount+= 1
  return tickCount

def updateOpticalSensor():
 print("Updating optical sensor boop")
 ##TODO IMPLEMENT THIS METHOD

def checkSensors():
  updateTickSensor()
  updateOpticalSensor()
  
def updateItems(tickDiff):
 print("Updating the items")
 #TODO IMPLEMENT THIS METHOD


def updateObjects():
 global tickCount
 global previousTickCount
 if (tickCount > previousTickCount):
  updateItems(tickCount-previousTickCount)
  previousTickCount = tickCount

def scanObjectEvent(scanString):
 global items;
 #TODO: IMPLEMENT THIS METHOD
 print("String scanned: {0}".format(scanString))
 
 item = getItem(scanString)
 if (item == False):
  item = Item(scanString)
  
  #call api
  URL = "http://54.163.253.131/conveyorscan/"
  URL = URL + scanString[1::]
 # PARAMS = {"isbn":scanString[1::]}

  response = requests.get(url=URL)
  data = response.json()
  print(data['slot'])
 else:
  item.Update()@jalkfdjdsakl
 
 

def readScanInput():
 global textScreen
 while(True):
  print("Scanning...")
  
  scan_str = input();
  scanObjectEvent(scan_str)
  



def mainLoop():
 global tickCount
 global scanBuffer
 

 scanThread = threading.Thread(target=readScanInput,args=(), daemon=True)
 scanThread.start()
 
 while True: # Run forever
  print("")
  checkConfigChanges()
  checkSensors()
  

  print("Tick count: {0}".format(tickCount))
  sleep(5)

#Execution starts here
setup()  
mainLoop()

