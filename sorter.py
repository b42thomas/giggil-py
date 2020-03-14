import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import threading
import queue
import curses
import time
import requests

rakes = [[0,12], [1,32], [2,53], [3,71]]

GPIO.setmode(GPIO.BOARD)
#pins
MOTOR_CONTROL_PINS = [7,11,13,15]
PUSHER_PINS = [8,18,22,40] #, 37] # red-8, green-16, blue-22, yellow-40, realpusher-37
TICK_SENSOR_PIN = 3
TRIP_SENSOR_PIN = 5

GPIO.setup(TICK_SENSOR_PIN, GPIO.IN)
GPIO.setup(TRIP_SENSOR_PIN, GPIO.IN)

for pin in PUSHER_PINS:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
  
for pin in MOTOR_CONTROL_PINS:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]


#global vars
opticalSensorTripped = False
tickStatus = 0
tickCount = 0
previousTickCount = tickCount
scanBuffer = ""
textScreen = curses.initscr()
FIRST_SCANNER_POSITION = -50
SECOND_SCANNER_POSITION = -15
OPTO_SENSOR_POSITION = 0


class Item:
 scanString = "phantom"
 ID = -1
 position = FIRST_SCANNER_POSITION
 slot = -1
 status = "Scan1" # 3 Statuses {Scan1, Scan2Verified, Scan2Exception, Tripped, TrippedException}
 
 def __init__(self,scanStr):
  self.scanString = scanStr
 def setId(newId):
  ID = newId
 

#def Update(

#items list
items = []

def getItem(scanString):
 global items
 for currentItem in items:
  if (currentItem.scanString == scanString):
   return currentItem
 return False

def getItem(scanString, scanStatus):
 global items
 for currentItem in items:
  if (currentItem.scanString == scanString) and (currentItem.status == scanStatus):
   return currentItem
 return False

def setup():
 print("setting up beep boop")
 global textScreen

 curses.noecho()
 curses.cbreak() 
 textScreen.keypad(True)

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
 #print("checking config changes boop boop")
 return

def updateTickSensor():
 global tickStatus
 global tickCount
 if (GPIO.input(TICK_SENSOR_PIN) != tickStatus):
  tickStatus = GPIO.input(TICK_SENSOR_PIN)
  if tickStatus == 1:
   tickCount += 1
   textScreen.addstr(2,0,"Tick Count:" + str(tickCount))
  
 return tickCount

def updateOpticalSensor():
 global opticalSensorTripped
 if GPIO.input(TRIP_SENSOR_PIN) == 1:
     opticalSensorTripped = False
 else:
     opticalSensorTripped = True
 textScreen.addstr(3,0,"Optical Sensor State:" + str(opticalSensorTripped))

def checkSensors():
  updateTickSensor()
  updateOpticalSensor()
  
def updateItems(tickDiff):
 global items
 i=0
 for currentItem in items:
  currentItem.position += tickDiff
  textScreen.addstr(6+i, 0, "Current Item: " + currentItem.scanString + " Position: " + str(currentItem.position)+"   Status: " + str(currentItem.status)+"   ") 
  i+=1


def updateObjects():
 global tickCount
 global previousTickCount
 if (tickCount > previousTickCount):
  updateItems(tickCount-previousTickCount)
  previousTickCount = tickCount
  
def createItem(scanString):
  #call api
  global items
  
  URL = "http://54.163.253.131/conveyorscan/"
  URL = URL + scanString + "?conveyorId=4"
   # PARAMS = {"isbn":scanString[1::]}

  response = requests.get(url=URL)
  data = response.json()
  
  item = Item(scanString)
  items.append(item)
  #item.id = data['id']
  item.slot = data['slot']
  
  
  return item


def firstScanEvent(scanString):
  item = createItem(scanString)
  item.status = "Scan1"
  
     #print(data)
  GPIO.output(PUSHER_PINS[int(item.slot)-1], GPIO.HIGH)
  textScreen.addstr(5,0,"Slot:" + item.slot)

  
def secondScanEvent(scanString):
 global items;
 #TODO: IMPLEMENT THIS METHOD
 textScreen.addstr(4,0,"String scanned: {0}".format(scanString))
 
 item = getItem(scanString, "Scan1")
 if (item == False):
  item = createItem(scanString)
  item.status = "Scan2Exception"
  item.position = SECOND_SCANNER_POSITION
  
 else:
     item.status = "Scan2Verified"
  
  #TODO MULTI-THREAD THIS API STUFF
  
   # TODO SET THE POSITION OF THE ITEM TO THE CORRECT SCANNER
 
def scanEvent(scanStr):
 if scanStr[0] == "A":
  firstScanEvent(scanStr[1::])
 else:
  secondScanEvent(scanStr[1::])

def readScanInput():
 global scanBuffer
 global textScreen
 scan_str = textScreen.getch()
 if(scan_str != -1):
  textScreen.addstr(1,0,"Scan Buffer: " + scanBuffer)
  if(scan_str in [curses.KEY_ENTER, ord('\n')]):
   scanEvent(scanBuffer)
   scanBuffer=""
  else:
   scanBuffer += chr(scan_str)
  



def mainLoop(textScreen):
 global tickCount

 textScreen.nodelay(True)

 scanThread = threading.Thread(target=readScanInput,args=(), daemon=True)
 scanThread.start()
 
 while True: # Run forever
  checkConfigChanges()
  checkSensors()
  readScanInput()
  updateObjects()
  
  for halfstep in range(8):
      for pin in range(4):
        GPIO.output(MOTOR_CONTROL_PINS[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.0009)

 textScreen.refresh()

  #print("Tick count: {0}".format(tickCount))
def main():
    setup()
    curses.wrapper(mainLoop)

if __name__ == "__main__":
    main()
    

GPIO.cleanup()

