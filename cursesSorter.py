#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import curses
import threading
import sys
from time import sleep # Import the sleep function from the time module

#pins
TICK_SENSOR_PIN = 11

#global vars
textScreen = curses.initscr()
#tickStatus = GPIO.LOW
tickStatus = 0
tickCount = 0
previousTickCount = tickCount
scanBuffer = ""
scan_str =""
 

def getInput(r, c, prompt_string):
    global textScreen
    curses.noecho()
    curses.raw() 
    textScreen.addstr(r, c, prompt_string)
    textScreen.refresh()
    myInp = textScreen.getstr(r + 1, c, 20)
    return myInp  #

def setup():
 print("setting up beep boop")
 global textScreen
 global tickCount
 curses.noecho()
 curses.cbreak() 
 textScreen.keypad(True)
 tickCount = 0
 #GPIO.setwarnings(False) # Ignore warning for now
 #GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
 #GPIO.setup(11, GPIO.OUT) # Set pin 8 to be an output pin and set initial value to low (off)
 #GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
 #pwm=GPIO.PWM(11, 50)
 #pwm.start(0)
 #tickStatus = GPIO.LOW

 
 
def checkConfigChanges():
 textScreen.addstr(0,0,"checking config changes boop boop")

def updateTickSensor():
 global tickStatus
 global tickCount
 tickCount+= 1
 return tickCount
# if (GPIO.input(TICK_SENSOR_PIN) != tickStatus):
#  tickStatus = GPIO.input(TICK_SENSOR_PIN)
  

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
 global scanBuffer
 scan_str = textScreen.getch()
 if(scan_str != -1):
  if(scan_str=13):
   scanObjectEvent(scanBuffer)
  else
   scanBuffer += chr(scan_str)
 
    
#  while (temp_char != '\n'):
#   temp_str = textScreen.getch()
#   if (temp_str != curses.ERR) :
#    scan_str += str(temp_str)
#    textScreen.addStr(6,0,scan_str)
#  scanObjectEvent(scan_str)
#  textScreen.addstr(5,0,"Sning: " + scan_str)
  



def mainLoop(textScreen):
 global tickCount
 global scanBuffer
 global scan_str 

 textScreen.nodelay(True)
 scanBuffer = ""
# scanThread = threading.Thread(target=readScanInput,args=(), daemon=True)
# scanThread.start()
 
 while True: # Run forever
  checkConfigChanges()
  checkSensors()
  readScanInput()

  tickCount+=1; #TODO REMOVE WHEN WE GET ENCODER
   
  textScreen.addstr(3,0,"Tick count: {0}".format(tickCount))
  textScreen.addstr(4,0,"Scan String22: " + scanBuffer)
 
  textScreen.refresh()
  


def main():
    setup()
    curses.wrapper(mainLoop)

if __name__ == "__main__":
    main()

#Execution starts here
setup()  
mainLoop()

#terminate curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
