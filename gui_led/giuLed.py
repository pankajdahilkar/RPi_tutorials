import tkinter as tk
import tkinter.font
import RPi.GPIO as GPIO
import time
LED = 40 # pin40
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # We are accessing GPIOs according to their physical location
GPIO.setup(LED, GPIO.OUT) # We have set our LED pin mode to output
GPIO.output(LED, GPIO.LOW) # When it will start then LED will be OFF
 
win=tk.Tk();
win.title("Led using gui")
myFont=tkinter.font.Font(family='Helvetica',size=12,weight="bold")


def ledToggle():
    if ledButton.config('text')[-1]=="Turn led off":
            ledButton["text"]="Turn LED On"
            print("LED OFF")
            GPIO.output(LED, GPIO.LOW) # led off

    else:
        led1=1
        ledButton["text"]="Turn led off"
        print("LED ON")
        GPIO.output(LED, GPIO.HIGH) # led on

def exitProgram():
    win.quit()
ledButton = tk.Button(win,text='Turn LED On',font=myFont,command=ledToggle,bg='bisque2',height=1,width=24)
ledButton.grid(row=0,sticky=tk.NSEW)
exitButton=tk.Button(win,text='Exit',font=myFont,command=exitProgram,bg='cyan',height=1,width=6)
exitButton.grid(row=1,sticky=tk.E)

tk.mainloop()
        
