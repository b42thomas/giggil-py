import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import curses
import threading
import queue
from time import sleep # Import the sleep function from the time module

#pins
TICK_SENSOR_PIN = 11

#global vars
textScreen = curses.initscr()
tickStatus = GPIO.LOW
tickCount = 0
previousTickCount = tickCount
scanBuffer = ""


#class Item:
# scanString
# ID
# pos
 
 #def Item(self,scanStr):
  #self.scanString = scanStr
 #def setId(newId):
  #ID = newId
 

def getInput(r, c, prompt_string):
    global textScreen
    curses.echo() 
    textScreen.addstr(r, c, prompt_string)
    textScreen.refresh()
    myInp = textScreen.getstr(r + 1, c, 20)
    return myInp  #

def setup():
 print("setting up beep boop")
 global textScreen
 curses.noecho()
 textScreen.nodelay(True)
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
 textScreen.addstr(0,0,"checking config changes boop boop")

def updateTickSensor():
 global tickStatus
 global tickCount
 if (GPIO.input(TICK_SENSOR_PIN) != tickStatus):
  tickStatus = GPIO.input(TICK_SENSOR_PIN)
  tickCount+= 1
  return tickCount

def updateOpticalSensor():
 textScreen.addstr(1,0,"Updating optical sensor boop")

def checkSensors():
  updateTickSensor()
  updateOpticalSensor()
  
def updateItems(tickDiff):
 book1Pos += tickDiff


def updateObjects():
 global tickCount
 global previousTickCount
 if (tickCount > previousTickCount):
  updateItems(tickCount-previousTickCount)
  previousTickCount = tickCount

def scanObjectEvent(scanString):
 print("h")  
 textScreen.addstr(4,0,"String scanned: {0}".format(scanString))
    
def readScanInput():
 while(True):
  textScreen.addstr(5,0,"SCanning: ")
  scan_str = input()
  scanObjectEvent(scan_str)
  textScreen.addstr(5,0,"Sning: " + scan_str)
  



def mainLoop():
 global tickCount
 global scanBuffer
 

 scanThread = threading.Thread(target=readScanInput,args=(), daemon=True)
 scanThread.start()
 scan_str = ""
 
 while True: # Run forever
  checkConfigChanges()
  checkSensors()
  tickCount+=1; #TODO REMOVE WHEN WE GET ENCODER

  textScreen.addstr(3,0,"Tick count: {0}".format(tickCount))
  
  #scan_str = getInput(4,0,"")
  
  scan_str += textScreen.getkey()
  textScreen.addstr(5,0,"Sning: " + scan_str)

  textScreen.refresh()
  


#Execution starts here
setup()  
mainLoop()
