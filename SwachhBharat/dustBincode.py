import RPi.GPIO as GPIO
import os
import time
import serial
ser = serial.Serial ("/dev/ttyUSB0", 9600)
GPIO_TRIGGER1 = 5
GPIO_ECHO1 = 7
GPIO_TRIGGER2 = 15
GPIO_ECHO2 = 13
dry_sens = 3
moist_sens = 11
# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E  = 24
LCD_D4 = 22
LCD_D5 = 18
LCD_D6 = 16
LCD_D7 = 12
 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
 
def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)       # Use BCM GPIO numbers
  GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
  GPIO.setup(GPIO_ECHO1, GPIO.IN)
  GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
  GPIO.setup(GPIO_ECHO2, GPIO.IN)
  GPIO.setup(dry_sens, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(moist_sens, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  # Initialise display
  
  os.system("aplay welcome.wav")
  while True:
    dist1 = distance1()
    dist2 = distance2()
    d1 = int(dist1)
    d2 = int(dist2)    
    dry_state =GPIO.input(dry_sens)
    wet_state = GPIO.input(moist_sens)
    # Send some test 
    ser.write("1Dist1="+d1+" cm"+"\n")
    ser.write("2Dist2="+d2+" cm"+"\n")
    print("Dist1="+dist1+" cm")
    print("Dist2="+dist2+" cm")
    time.sleep(2) # 3 second delay
    s1="Dry"
    s2="Dry"
    if wet_state == False:
        s1="wet"
    else :
        s1="Dry"
    if dry_state == False:
        s2="wet"
    else :
        s2="Dry"
        
    print("wet_state =" + s1)
    print("dry_state ="+ s2)
    # Send some text
    ser.write("1wet_state=" + s1+"\n")
    ser.write ("2dry_state="+ s2+"\n")
    time.sleep(2) # 3 second delay
    if(d1 < 7 and d1 > 0):
          ser.write ("1Welcome \n")
          ser.write("2Dry Waste \n")
          os.system("aplay welcome.wav")
          time.sleep(2)
          os.system("aplay left.wav")
          time.sleep(2)
          os.system("aplay right.wav")
          dry_state =GPIO.input(dry_sens)
          if dry_state == False:
                    os.system("aplay left.wav")
          else :
              s2="Dry"
              os.system("aplay wifi.wav")
              ser.write ("1Password \n")
              ser.write("2digitalindia \n")
              time.sleep(6)
              os.system("aplay thank.wav")
              ser.write ("1Thank You \n")
              ser.write ("2 Have nice day \n")
              os.system("aplay wish.wav")

    if(d2 < 7 and d2 > 0):
          ser.write ("1Welcome \n")
          ser.write("2Wet Waste \n")
          os.system("aplay welcome.wav")
          time.sleep(2)
          os.system("aplay left.wav")
          time.sleep(2)
          os.system("aplay right.wav")
          wet_state =GPIO.input(wet_sens)
          if dry_state == True:
                    os.system("aplay right.wav")
          else :
              s2="Dry"
              os.system("aplay wifi.wav")
              ser.write ("1Password \n")
              ser.write("2digitalindia \n")
              time.sleep(6)
              os.system("aplay thank.wav")
              ser.write ("1Thank You \n")
              ser.write ("2 Have nice day \n")
              os.system("aplay wish.wav")

    
def distance1():
    GPIO.output(GPIO_TRIGGER1, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER1, False)
    StartTime1 = time.time()
    StopTime1 = time.time()
    while GPIO.input(GPIO_ECHO1) == 0:
        StartTime1 = time.time()
    while GPIO.input(GPIO_ECHO1) == 1:
        StopTime1 = time.time()
    TimeElapsed1 = StopTime1 - StartTime1
    distance1 = (TimeElapsed1 * 34300) / 2
    return (distance1)

def distance2():
    GPIO.output(GPIO_TRIGGER2, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER2, False)
    StartTime2 = time.time()
    StopTime2 = time.time()
    while GPIO.input(GPIO_ECHO2) == 0:
        StartTime2 = time.time()
    while GPIO.input(GPIO_ECHO2) == 1:
        StopTime2 = time.time()
    TimeElapsed2 = StopTime2 - StartTime2
    distance2 = (TimeElapsed2 * 34300) / 2
    return (distance2)


if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    GPIO.cleanup()
