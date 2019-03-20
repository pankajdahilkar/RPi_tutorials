import RPi.GPIO as GPIO
import os
import time

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
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
  GPIO.setup(GPIO_ECHO1, GPIO.IN)
  GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
  GPIO.setup(GPIO_ECHO2, GPIO.IN)
  GPIO.setup(dry_sens, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(moist_sens, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  # Initialise display
  lcd_init()
  os.system("aplay welcome.wav")
  while True:
    dist1 = distance1()
    dist2 = distance2()
    dry_state =GPIO.input(dry_sens)
    wet_state = GPIO.input(moist_sens)
    # Send some test
    lcd_display(0x01,LCD_CMD)
    lcd_string("Dist1="+dist1+" cm",LCD_LINE_1)
    lcd_string("Dist1="+dist1+" cm",LCD_LINE_2)
    
    time.sleep(2) # 3 second delay
 
    # Send some text
    lcd_display(0x01,LCD_CMD)
    lcd_string("wet_state " + str(wet_state),LCD_LINE_1)
    lcd_string("dry_state"+ str(dry_state),LCD_LINE_2)

    time.sleep(2) # 3 second delay

      
def lcd_init():
  lcd_display(0x28,LCD_CMD) # Selecting 4 - bit mode with two rows
  lcd_display(0x0C,LCD_CMD) # Display On,Cursor Off, Blink Off
  lcd_display(0x01,LCD_CMD) # Clear display

  time.sleep(E_DELAY)
 
def lcd_display(bits, mode):
  # Send byte to data pins
  
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_display(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_display(ord(message[i]),LCD_CHR)
    time.sleep(0.001)

    
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
    return str(distance1)

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
    return str(distance2)


if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_display(0x01, LCD_CMD)
    GPIO.cleanup()
