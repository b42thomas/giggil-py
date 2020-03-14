  
  
import RPi.GPIO as GPIO
import time
import curses
GPIO.setmode(GPIO.BOARD)

textScreen = curses.initscr()

control_pins = [7,11,13,15]
pusher_pins = [8,18,22,40, 37] # red-8, green-16, blue-22, yellow-40, realpusher-37
tickSensor_pin = 3
tripSensor_pin = 5

GPIO.setup(tickSensor_pin, GPIO.IN)
GPIO.setup(tripSensor_pin, GPIO.IN)

for pin in pusher_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
  
for pin in control_pins:
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

    
while True:
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.0009)
    reflected = GPIO.input(tickSensor_pin)
    tripped = GPIO.input(tripSensor_pin)
    textScreen.addstr(0,0, "Tick:" + str(reflected))
    textScreen.addstr(1,0, "Tripped:" + str(tripped))
    textScreen.refresh()

for x in range(4):
  GPIO.output(pusher_pins[x], GPIO.HIGH)
  time.sleep(1)
GPIO.cleanup()